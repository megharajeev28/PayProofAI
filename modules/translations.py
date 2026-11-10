LANGUAGES = {
    "Malayalam": {"code":"ml-IN"},
    "English": {"code":"en-IN"},
    "Hindi": {"code":"hi-IN"},
    "Tamil": {"code":"ta-IN"},
    "Kannada": {"code":"kn-IN"},
    "Telugu": {"code":"te-IN"},
}

LESSONS = [
    ("Never share OTPs", "An OTP can authorise access or a transaction. A genuine support agent should not ask you to disclose it.", "A caller says an OTP is needed to release a customer payment.", "End the call and contact the bank using its official channel.", "Read the OTP aloud or forward it."),
    ("Never share your UPI PIN", "Your UPI PIN is used to authorise payments from your account.", "A stranger asks you to enter your PIN to receive a refund.", "Enter the PIN only in your trusted app when you intend to pay.", "Tell anyone your PIN or enter it because a caller asks."),
    ("QR codes do not receive money", "Scanning a QR code and entering your PIN can authorise a payment.", "A buyer sends a QR code and says scan it to collect the sale amount.", "Ask the buyer to pay through their own app and verify the credit.", "Scan an unknown QR code to receive money."),
    ("Do not trust screenshots alone", "Images and messages can be copied, edited or delayed.", "A customer shows a success screen but your balance is unchanged.", "Check your own bank app and transaction history.", "Hand over goods based only on a screenshot."),
    ("Check your actual account", "The trusted source for your credit is your bank or official payment app.", "A message says money was transferred, but no credit appears.", "Open the bank app yourself and verify amount and transaction.", "Click a link in an unsolicited message to check balance."),
    ("Avoid unknown screen-sharing apps", "Remote access can expose sensitive information and let scammers control your device.", "A caller asks you to install a support app and share your screen.", "Stop and call the bank using its official number.", "Install remote-control apps at a stranger's request."),
    ("Ignore pressure from suspicious callers", "Scammers may create urgency to stop you checking independently.", "Someone says release goods immediately or the payment will reverse.", "Pause, verify independently and keep a record of the interaction.", "Let urgency override your normal payment checks."),
]

def safety_lessons(language="English"):
    if language == "Malayalam":
        return [
            {"title":"OTP ആരോടും പങ്കിടരുത്","why":"OTP നിങ്ങളുടെ അക്കൗണ്ടിലേക്കുള്ള പ്രവേശനമോ ഇടപാടോ അനുവദിക്കാം.","example":"പണം റിലീസ് ചെയ്യാൻ OTP വേണമെന്ന് ഒരാൾ പറയുന്നു.","do":"വിളി അവസാനിപ്പിച്ച് ഔദ്യോഗിക ബാങ്ക് മാർഗം ബന്ധപ്പെടുക.","avoid":"OTP വായിച്ചുകൊടുക്കുകയോ ഫോർവേഡ് ചെയ്യുകയോ ചെയ്യരുത്."},
            {"title":"UPI PIN രഹസ്യമായി സൂക്ഷിക്കുക","why":"നിങ്ങളുടെ അക്കൗണ്ടിൽ നിന്ന് പണം അയയ്ക്കാൻ PIN ഉപയോഗിക്കുന്നു.","example":"റീഫണ്ട് ലഭിക്കാൻ PIN നൽകണമെന്ന് പറയുന്നു.","do":"നിങ്ങൾ സ്വയം പണമടയ്ക്കുമ്പോൾ മാത്രം വിശ്വസനീയ ആപ്പിൽ PIN നൽകുക.","avoid":"PIN ആരോടും പറയരുത്."},
            {"title":"പണം സ്വീകരിക്കാൻ QR സ്കാൻ ചെയ്യരുത്","why":"QR സ്കാൻ ചെയ്ത് PIN നൽകുന്നത് പണമടയ്ക്കാൻ ഇടയാക്കാം.","example":"വാങ്ങുന്നയാൾ പണം ലഭിക്കാൻ QR സ്കാൻ ചെയ്യാൻ പറയുന്നു.","do":"സ്വന്തം ആപ്പിൽ ക്രെഡിറ്റ് വന്നോ പരിശോധിക്കുക.","avoid":"അപരിചിത QR സ്കാൻ ചെയ്യരുത്."},
            {"title":"സ്ക്രീൻഷോട്ട് മാത്രം തെളിവല്ല","why":"ചിത്രം പകർത്താനോ മാറ്റാനോ കഴിയും.","example":"സ്ക്രീനിൽ വിജയമെന്ന് കാണിക്കുന്നു, പക്ഷേ ബാലൻസ് മാറിയിട്ടില്ല.","do":"സ്വന്തം ബാങ്ക് ആപ്പിൽ പരിശോധിക്കുക.","avoid":"സ്ക്രീൻഷോട്ട് മാത്രം കണ്ട് സാധനം കൈമാറരുത്."},
            {"title":"യഥാർത്ഥ അക്കൗണ്ട് പരിശോധിക്കുക","why":"നിങ്ങളുടെ ബാങ്ക് ആപ്പിലെ ക്രെഡിറ്റാണ് പരിശോധിക്കേണ്ടത്.","example":"SMS വന്നെങ്കിലും പണം അക്കൗണ്ടിൽ കാണുന്നില്ല.","do":"ബാങ്ക് ആപ്പ് സ്വയം തുറന്ന് ഇടപാട് പരിശോധിക്കുക.","avoid":"അറിയാത്ത ലിങ്കിൽ ക്ലിക്ക് ചെയ്യരുത്."},
            {"title":"അപരിചിത സ്ക്രീൻ-ഷെയറിംഗ് ഒഴിവാക്കുക","why":"റിമോട്ട് ആപ്പ് വഴി നിങ്ങളുടെ ഫോൺ നിയന്ത്രിക്കപ്പെടാം.","example":"സഹായത്തിനായി ഒരു ആപ്പ് ഇൻസ്റ്റാൾ ചെയ്യാൻ വിളിക്കുന്നയാൾ പറയുന്നു.","do":"വിളി നിർത്തി ഔദ്യോഗിക ബാങ്ക് നമ്പറിൽ ബന്ധപ്പെടുക.","avoid":"അപരിചിതർ പറയുന്ന ആപ്പുകൾ ഇൻസ്റ്റാൾ ചെയ്യരുത്."},
            {"title":"സമ്മർദ്ദത്തിന് വഴങ്ങരുത്","why":"വേഗത്തിൽ തീരുമാനിപ്പിക്കാൻ തട്ടിപ്പുകാർ ശ്രമിക്കാം.","example":"ഉടൻ സാധനം നൽകണമെന്ന് ഒരാൾ നിർബന്ധിക്കുന്നു.","do":"നിർത്തി സ്വതന്ത്രമായി പണം പരിശോധിക്കുക.","avoid":"തിരക്കിൽ സുരക്ഷാ പരിശോധന ഒഴിവാക്കരുത്."},
        ]
    return [{"title":t,"why":w,"example":e,"do":d,"avoid":a} for t,w,e,d,a in LESSONS]
