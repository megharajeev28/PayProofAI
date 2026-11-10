# PayProof AI — Think Before You Trust

A Malayalam-first, multilingual payment safety companion for small merchants and everyday users. It analyses message wording for explainable warning indicators, reviews visible screenshot details, offers a local safety Q&A assistant, and can use Gnani Prisma STT and Timbre TTS when credentials and a compatible SDK are available.

> **Critical boundary:** PayProof AI is not connected to a bank or UPI provider. It cannot confirm a transaction, authenticate a screenshot, or prove fraud. Always check the credit in your own bank account or official payment application.

## Features

- Six language choices: Malayalam (default), English, Hindi, Tamil, Kannada and Telugu.
- Voice recording/transcription using the supplied JanVoice-compatible Gnani client calls.
- Spoken responses using Gnani Timbre v2.5.
- Explainable rule-based message indicators: OTP/PIN requests, QR receive claims, suspicious links, refund language, urgency, remote access and payment claims.
- JPG/PNG screenshot review, optional OCR, manual description fallback and visible-detail checklist.
- Local safety Q&A, bilingual Malayalam/English guide, simulated demo cases.
- Session-only chat and no permanent screenshot storage.
- Demo mode works without an API key.

## Requirements

- Python 3.11 or newer.
- Gnani Vachana SDK access and API key for voice features.
- Optional OCR: `pytesseract` Python package **and** the Tesseract OCR system executable. OCR is not required.

## Windows PowerShell — install and run

```powershell
cd path\to\PayProofAI
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Add your Gnani API key

Create `.streamlit/secrets.toml` (this file is ignored by Git):

```toml
GNANI_API_KEY = "YOUR_GNANI_API_KEY"
```

Alternatively, set an environment variable for the current PowerShell session:
```powershell
$env:GNANI_API_KEY = "YOUR_GNANI_API_KEY"
streamlit run app.py
```

Restart Streamlit after adding/changing the key. The app only displays whether a key is configured; it never displays the key. **Do not upload `secrets.toml` to GitHub.**

## Gnani SDK compatibility notes

The implementation uses the JanVoice interface specified for this build:
- `from gnani.stt import GnaniSTTClient`
- `from gnani.tts import GnaniTTSClient, AudioConfig`
- `GnaniSTTClient(api_key=...).transcribe(path, language_code=...)`
- `GnaniTTSClient(api_key=...).synthesize(text, voice="Nalini", model="timbre-v2.5", language=..., speed=1.0, audio_config=AudioConfig(...))`

The SDK package is declared as `gnani-vachana`. SDK package releases and response payload formats can change; verify against the exact package/version provided in your Gnani developer account if imports or method signatures differ. The app reports SDK errors and keeps text features usable. Audio input is written to a temporary file and removed after transcription. TTS output is expected to be WAV bytes.

Evon v3.3 is intentionally not called: no verified endpoint or credentials/configuration were supplied. No model connection is simulated.

## Optional OCR setup

Install Tesseract OCR for Windows from its official distribution, then:
```powershell
pip install pytesseract
```
If Tesseract is not on PATH, configure `pytesseract.pytesseract.tesseract_cmd` in `modules/image_inspector.py` to the installed executable location. Without it, manual description still works.

## GitHub upload

```powershell
git init
git add .
git status
git commit -m "Build PayProof AI payment safety assistant"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/PayProofAI.git
git push -u origin main
```
Check `git status` and confirm `.streamlit/secrets.toml` is not staged before pushing.

## Streamlit Community Cloud deployment

1. Push the project to GitHub without secrets.
2. In Streamlit Community Cloud, create an app from the repository and set the main file to `app.py`.
3. Open the app's **Settings → Secrets**.
4. Add:
   ```toml
   GNANI_API_KEY = "YOUR_GNANI_API_KEY"
   ```
5. Save and reboot the app. Without the key, text-based demo functionality still runs.

## Demo walkthrough (about 2 minutes)

1. Open Home and show Malayalam as the default language.
2. Select simulated Scenario A. Explain the payment claim, link and pressure indicators.
3. Open Check a Payment Message and paste: `Bank support: share your OTP to release the pending UPI payment immediately.` Show the HIGH indicator and safe next steps.
4. Open Inspect Payment Screenshot. Upload a sample image with personal information blurred. Explain that OCR only reads visible words and cannot authenticate payment.
5. Ask PayProof: “A customer showed a screenshot but my balance has not changed. What should I do?”
6. Finish with the principle: “A screenshot is not proof. Verify the credit in your own bank app.”

## Troubleshooting

- **Missing API key:** create `.streamlit/secrets.toml` or set `GNANI_API_KEY`; text mode remains available.
- **`No module named gnani`:** activate the correct virtual environment and install the Gnani package available to your account. Confirm the package distribution name with your SDK documentation.
- **STT/TTS import or authentication error:** check the SDK package/version, key validity, account access and provider status. The app shows a meaningful error and continues in text mode.
- **Empty transcription:** record clearly, check microphone permissions and try again.
- **TTS audio not playable:** confirm the SDK returns WAV bytes for the requested `AudioConfig`; check SDK version and output container.
- **OCR unavailable:** install Tesseract and optional `pytesseract`, or use the manual description field.
- **Upload rejected:** use a JPG/PNG image smaller than 8 MB.

## Privacy and safety

- Screenshots are processed in memory and are not saved by this application.
- Audio is sent to Gnani when you explicitly request transcription; temporary local audio files are removed after the request.
- Do not submit sensitive banking information. Blur names, phone numbers and UPI IDs.
- No OTP, UPI PIN, password or full card number is requested.
- This app does not claim end-to-end encryption, bank access, transaction confirmation, image authenticity or fraud certainty.
- Suspected cyber financial fraud in India: contact the national cybercrime helpline **1930** promptly or use the official [National Cyber Crime Reporting Portal](https://cybercrime.gov.in/).

## Project layout

```text
PayProofAI/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .streamlit/config.toml
├── modules/
│   ├── __init__.py
│   ├── gnani_service.py
│   ├── voice_service.py
│   ├── payment_analyzer.py
│   ├── image_inspector.py
│   ├── safety_knowledge.py
│   └── translations.py
└── assets/logo.svg
```
