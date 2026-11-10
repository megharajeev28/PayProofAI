DEMO_SCENARIOS = {
    "A — Fake UPI payment confirmation": {
        "input": "I have sent ₹2,500. Payment successful. Check this screenshot and release the goods immediately: http://upi-refund-example.test",
        "indicators": ["Payment-success claim", "External link", "Urgency to release goods"],
        "response": "Do not rely on the sender's screenshot or message. Open your own bank or official UPI app and check whether ₹2,500 is credited.",
        "next_steps": ["Do not open the link.", "Check your own transaction history.", "Hand over goods only after confirming the credit in your account."]
    },
    "B — Screenshot but no credit": {
        "input": "The customer showed a successful payment screenshot, but the money is not in my account.",
        "indicators": ["Third-party screenshot is the only evidence", "Merchant has not independently verified credit"],
        "response": "A screenshot alone is not proof. Ask the customer to wait while you check your own bank app. A delay can happen and does not by itself prove fraud.",
        "next_steps": ["Refresh/check your bank app and transaction history.", "Do not hand over goods until credit appears.", "If still unresolved, contact your bank through official channels."]
    },
    "C — OTP to release payment": {
        "input": "A caller says they are bank support and needs my OTP to release a payment.",
        "indicators": ["OTP request", "Claimed bank/support identity", "Payment-release pretext"],
        "response": "Never share the OTP. End the call and contact your bank using an official number or app.",
        "next_steps": ["Do not disclose the code.", "Do not install an app or share your screen.", "If already shared, contact your bank immediately and report suspected cyber fraud through official channels."]
    }
}

def answer_question(question, language="English", history=None):
    q = (question or "").lower()
    if any(x in q for x in ["otp", "one-time", "ഒടിപി", "ओटीपी"]):
        en = "Never share an OTP with a caller, customer or person claiming to be bank support. End the interaction and contact your bank through its official app or number. If you already shared it, contact the bank immediately and report suspected cyber financial fraud through official channels."
    elif any(x in q for x in ["pin", "upi pin", "പിൻ"]):
        en = "Never tell anyone your UPI PIN. Enter it only inside your trusted UPI app when you are intentionally making a payment. You do not need to enter a PIN to receive money."
    elif any(x in q for x in ["qr", "ക്യുആർ"]):
        en = "Be careful: scanning a QR code and entering your UPI PIN usually authorises a payment from you. Do not scan a stranger's QR code to receive money."
    elif any(x in q for x in ["screenshot", "സ്ക്രീൻഷോട്ട്"]):
        en = "A screenshot can be copied or altered and cannot prove that money reached you. Open your own bank or official UPI app and verify the credited transaction. If no credit appears, wait and do not release goods yet."
    elif any(x in q for x in ["pending", "delay", "വൈകി"]):
        en = "A pending or delayed payment is not automatically fraud. Check your own bank transaction history, ask the customer to check their app, and wait for the credit to appear before handing over goods. Contact your bank if it remains unresolved."
    elif any(x in q for x in ["successful", "received", "credited", "payment"]):
        en = "To check a payment, open your own bank app or official UPI app independently and look for the credited transaction and amount. Do not rely only on SMS, a caller or a screenshot. PayProof AI cannot access your bank account or confirm a transfer."
    else:
        en = "Pause before acting. Never share OTPs, UPI PINs or passwords; do not scan a QR code to receive money or install remote-access apps. Verify payment directly in your own bank app and contact your bank through official channels if unsure."
    if language == "Malayalam":
        return "ശ്രദ്ധിക്കുക. " + {
            "otp": "OTP ആരോടും പങ്കിടരുത്. ബാങ്ക് ഉദ്യോഗസ്ഥനെന്ന് പറയുന്ന ആളോടുപോലും നൽകരുത്. സംശയമുണ്ടെങ്കിൽ ഔദ്യോഗിക ബാങ്ക് ആപ്പ് വഴിയോ ഔദ്യോഗിക നമ്പർ വഴിയോ ബാങ്കിനെ ബന്ധപ്പെടുക.",
            "pin": "UPI PIN ആരോടും പറയരുത്. നിങ്ങൾ സ്വയം പണമടയ്ക്കുമ്പോൾ മാത്രം വിശ്വസനീയമായ UPI ആപ്പിൽ നൽകുക. പണം സ്വീകരിക്കാൻ PIN നൽകേണ്ടതില്ല.",
            "qr": "QR കോഡ് സ്കാൻ ചെയ്ത് പണം സ്വീകരിക്കാമെന്ന വാദം വിശ്വസിക്കരുത്. QR സ്കാൻ ചെയ്ത് PIN നൽകുന്നത് നിങ്ങളുടെ അക്കൗണ്ടിൽ നിന്ന് പണം അയയ്ക്കാൻ ഇടയാക്കാം.",
            "screenshot": "സ്ക്രീൻഷോട്ട് മാത്രം പണം ലഭിച്ചതിന്റെ തെളിവല്ല. നിങ്ങളുടെ സ്വന്തം ബാങ്ക് ആപ്പിൽ ക്രെഡിറ്റ് പരിശോധിക്കുക. പണം കാണുന്നതുവരെ സാധനം കൈമാറരുത്.",
            "default": "നിങ്ങളുടെ സ്വന്തം ബാങ്ക് ആപ്പിലോ ഔദ്യോഗിക UPI ആപ്പിലോ ഇടപാട് പരിശോധിക്കുക. OTP, UPI PIN, പാസ്‌വേഡ് എന്നിവ ആരോടും പങ്കിടരുത്. PayProof AI-ക്ക് നിങ്ങളുടെ ബാങ്ക് അക്കൗണ്ട് പരിശോധിക്കാനാവില്ല."
        }.get("otp" if "otp" in q else "pin" if "pin" in q else "qr" if "qr" in q else "screenshot" if "screenshot" in q else "default")
    if language == "Hindi":
        return "सावधान रहें। OTP या UPI PIN किसी के साथ साझा न करें। भुगतान की पुष्टि अपने बैंक या आधिकारिक UPI ऐप में स्वयं करें। स्क्रीनशॉट भुगतान का प्रमाण नहीं है। PayProof AI आपके बैंक खाते की जाँच नहीं कर सकता।"
    if language == "Tamil":
        return "கவனமாக இருங்கள். OTP அல்லது UPI PIN-ஐ யாரிடமும் பகிர வேண்டாம். உங்கள் வங்கி அல்லது அதிகாரப்பூர்வ UPI செயலியில் பணம் வந்துள்ளதா என நீங்களே சரிபார்க்கவும். ஸ்கிரீன்ஷாட் பணம் வந்ததற்கான ஆதாரம் அல்ல."
    if language == "Kannada":
        return "ಎಚ್ಚರಿಕೆಯಿಂದಿರಿ. OTP ಅಥವಾ UPI PIN ಅನ್ನು ಯಾರೊಂದಿಗೂ ಹಂಚಿಕೊಳ್ಳಬೇಡಿ. ನಿಮ್ಮ ಬ್ಯಾಂಕ್ ಅಥವಾ ಅಧಿಕೃತ UPI ಆ್ಯಪ್‌ನಲ್ಲಿ ಹಣ ಜಮೆಯಾಗಿದೆಯೇ ಎಂದು ನೀವೇ ಪರಿಶೀಲಿಸಿ. ಸ್ಕ್ರೀನ್‌ಶಾಟ್ ಪಾವತಿಯ ಸಾಕ್ಷ್ಯವಲ್ಲ."
    if language == "Telugu":
        return "జాగ్రత్తగా ఉండండి. OTP లేదా UPI PIN ను ఎవరితోనూ పంచుకోవద్దు. మీ బ్యాంక్ లేదా అధికారిక UPI యాప్‌లో డబ్బు జమైందో లేదో స్వయంగా తనిఖీ చేయండి. స్క్రీన్‌షాట్ చెల్లింపుకు రుజువు కాదు."
    return en
