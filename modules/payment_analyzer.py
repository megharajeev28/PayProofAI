import re
from typing import List
from pydantic import BaseModel, Field

class AnalysisResult(BaseModel):
    risk_level: str
    category: str
    indicators: List[str] = Field(default_factory=list)
    explanation: str
    recommended_actions: List[str]
    never_do: List[str]
    confidence_note: str = "Indicator-based guidance only. This is not proof of fraud or transaction status."

RULES = [
    ("OTP_REQUEST", r"\b(otp|one[- ]time password|verification code)\b", "The message mentions an OTP or verification code.", "HIGH"),
    ("UPI_PIN_REQUEST", r"\b(upi pin|pin number|enter your pin|share your pin)\b", "The sender appears to request a UPI PIN.", "HIGH"),
    ("REMOTE_ACCESS", r"\b(anydesk|teamviewer|quick.?support|screen.?share|remote access)\b", "A remote-access or screen-sharing app is mentioned.", "HIGH"),
    ("QR_RECEIVE_SCAM", r"\b(scan (this )?(qr|code)|scan qr).{0,45}\b(receive|get|claim|collect)\b|\b(receive|get) money.{0,35}\b(scan|qr)\b", "Scanning a QR code is presented as a way to receive money.", "HIGH"),
    ("SUSPICIOUS_LINK", r"https?://|www\.", "The message contains a web link. Check its destination independently.", "CAUTION"),
    ("URGENCY", r"\b(immediately|urgent|right now|hurry|last chance|release (the )?(goods|item))\b", "The sender is applying urgency or pressure.", "CAUTION"),
    ("REFUND_SCAM", r"\b(refund|cashback|reversal)\b.{0,70}\b(pin|otp|scan|link|install)\b|\b(pin|otp|scan|link|install)\b.{0,70}\b(refund|cashback|reversal)\b", "A refund or cashback is linked to a risky action.", "HIGH"),
    ("PAYMENT_CLAIM", r"\b(payment (is )?(done|successful|completed)|paid you|sent the money|transfer successful)\b", "The sender claims that a payment has been made.", "CAUTION"),
    ("IMPERSONATION", r"\b(bank support|upi support|payment support|customer care|bank officer)\b", "The sender claims to represent a bank or payment support.", "CAUTION"),
]

def analyze_message(message: str, language="English") -> AnalysisResult:
    text = message or ""
    hits = []
    categories = []
    for category, pattern, explanation, level in RULES:
        if re.search(pattern, text, re.I | re.S):
            hits.append(explanation); categories.append((category, level))
    if any(level == "HIGH" for _, level in categories): risk = "HIGH"
    elif categories: risk = "CAUTION"
    else: risk = "LOW"
    if "OTP_REQUEST" in [x[0] for x in categories] or "UPI_PIN_REQUEST" in [x[0] for x in categories]:
        explanation = "Do not disclose an OTP or UPI PIN to anyone. Stop and verify through your bank's official app or contact channel."
    elif "QR_RECEIVE_SCAM" in [x[0] for x in categories]:
        explanation = "A QR scan is generally used to make a payment, not to receive one. Do not scan it to collect money."
    elif "PAYMENT_CLAIM" in [x[0] for x in categories]:
        explanation = "A sender's claim or message does not establish that funds reached your account. Check your own bank or official payment app."
    elif hits:
        explanation = "One or more patterns deserve caution. These indicators do not prove the message is fraudulent; verify using a trusted, independent channel."
    else:
        explanation = "No configured warning pattern was detected. This does not prove the message is genuine or that a payment succeeded."
    actions = [
        "Open your bank app or official UPI app yourself and check the credited transaction and balance.",
        "If details remain unclear, contact your bank using the number on its official website or card.",
        "Do not hand over goods until the credit appears in your own account."
    ]
    if risk == "HIGH":
        actions.insert(0, "Stop interacting with the sender and do not follow the requested action.")
    never = ["Never share an OTP, UPI PIN, banking password or card security code.", "Never install an app or scan a QR code because a stranger instructs you to."]
    return AnalysisResult(risk_level=risk, category=categories[0][0] if categories else "NO_MATCH", indicators=hits,
        explanation=explanation, recommended_actions=actions, never_do=never)
def analyze_payment_context(message, *args, **kwargs):
    return analyze_message(message)