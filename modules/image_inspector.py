import io, re
from PIL import Image

def inspect_image(image_bytes, declared_format, manual_description=""):
    observations = []
    extracted = ""
    ocr_note = ""
    image = Image.open(io.BytesIO(image_bytes))
    if image.format not in ("JPEG", "PNG"):
        raise ValueError("Only JPG, JPEG and PNG images are supported.")
    try:
        import pytesseract
        extracted = pytesseract.image_to_string(image).strip()
        if not extracted: ocr_note = "OCR ran but could not read clear text. You can describe the screenshot manually."
    except Exception:
        ocr_note = "Optional OCR is unavailable (pytesseract and/or the Tesseract system binary is missing). Manual description remains available."
    content = (extracted + "\n" + (manual_description or "")).strip()
    patterns = {
        "transaction/reference ID": r"\b(UTR|UPI|RRN|txn|transaction)\s*(id|no|number|ref)?\s*[:#-]?\s*[A-Z0-9]{6,}\b",
        "amount": r"(₹|INR|Rs\.?)\s?[\d,]+(?:\.\d{1,2})?",
        "date or time": r"\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b|\b\d{1,2}:\d{2}\b",
        "payment status wording": r"\b(success|successful|completed|pending|failed|processing)\b",
    }
    found = []
    for label, pattern in patterns.items():
        if re.search(pattern, content, re.I): found.append(label)
    if found: observations.append("Visible text appears to include: " + ", ".join(found) + ".")
    missing = [name for name in ("transaction/reference ID", "amount", "date or time", "payment status wording") if name not in found]
    if missing: observations.append("Not detected in readable text: " + ", ".join(missing) + ". This may be due to cropping, image quality or OCR limitations.")
    if re.search(r"\b(successful|completed)\b", content, re.I):
        observations.append("The image text claims a successful/completed status. This wording cannot confirm that your account was credited.")
    if re.search(r"\b(pending|processing|failed)\b", content, re.I):
        observations.append("The visible status includes pending, processing or failed wording; check the transaction independently.")
    if manual_description.strip():
        observations.append("Manual description was considered as context, not as independently verified transaction data.")
    if not observations: observations.append("No reliable payment details could be extracted. Review the image manually and verify through your own bank app.")
    return {"extracted_text": extracted, "observations": observations, "ocr_note": ocr_note}
