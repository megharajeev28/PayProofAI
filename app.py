import os
import streamlit as st
from PIL import Image
from modules.translations import LANGUAGES, safety_lessons
from modules.gnani_service import get_api_key, get_clients, sdk_status
from modules.voice_service import transcribe_audio, synthesize_speech
from modules.payment_analyzer import analyze_message, analyze_payment_context
from modules.image_inspector import inspect_image
from modules.safety_knowledge import answer_question, DEMO_SCENARIOS

st.set_page_config(page_title="PayProof AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'DM Sans',sans-serif;}
.stApp {background:linear-gradient(135deg,#071827 0%,#0b2634 42%,#f3f7f8 42%,#f3f7f8 100%);}
.block-container {padding-top:1.5rem; max-width:1250px;}
.hero {background:linear-gradient(120deg,#092334,#0b4b50); padding:30px 34px; border-radius:22px; color:white; box-shadow:0 12px 35px #00192333;}
.hero h1 {font-size:2.5rem; letter-spacing:1px; margin:0; color:white;}
.hero p {color:#d5e9e9; margin:.4rem 0 0 0;}
.panel {background:white; border:1px solid #e4ecee; border-radius:18px; padding:22px; box-shadow:0 5px 18px #102d3810; margin-bottom:14px;}
.metric {background:#fff; border:1px solid #e5ecee; border-radius:16px; padding:18px;}
.small {color:#657781; font-size:.9rem;}
.warning {background:#fff4df; border-left:5px solid #e9a329; border-radius:12px; padding:14px 17px; color:#553b12;}
.safe {background:#e8f7ef; border-left:5px solid #15965b; border-radius:12px; padding:14px 17px; color:#155b3a;}
.danger {background:#fff0ef; border-left:5px solid #d94b43; border-radius:12px; padding:14px 17px; color:#79231e;}
.stButton>button {border-radius:12px; font-weight:700; min-height:2.7rem;}
[data-testid="stSidebar"] {background:#071c2a;}
[data-testid="stSidebar"] * {color:#e7f0f2;}
h2,h3 {color:#0c2938;}
</style>
""", unsafe_allow_html=True)

if "language" not in st.session_state: st.session_state.language = "Malayalam"
if "messages" not in st.session_state: st.session_state.messages = []
if "latest_analysis" not in st.session_state: st.session_state.latest_analysis = None
if "chat_input" not in st.session_state: st.session_state.chat_input = ""

lang_name = st.session_state.language
lang_code = LANGUAGES[lang_name]["code"]
api_key = get_api_key()
stt_ok, tts_ok, sdk_message = sdk_status()

with st.sidebar:
    st.markdown("## 🛡️ PAYPROOF AI")
    st.caption("Think Before You Trust.")
    page = st.radio("NAVIGATION", ["Home", "Check a Payment Message", "Inspect Payment Screenshot", "Ask PayProof", "Safety Guide", "About"], label_visibility="collapsed")
    st.divider()
    st.selectbox("Language / ഭാഷ", list(LANGUAGES), key="language")
    st.caption("Voice API: " + ("Configured" if api_key else "Demo mode — key not set"))
    if st.button("Clear this session", use_container_width=True):
        st.session_state.messages = []
        st.session_state.latest_analysis = None
        st.rerun()
    st.markdown("---")
    st.caption("Never share an OTP, UPI PIN or banking password.")

def section_header(title, subtitle=""):
    st.markdown(f"### {title}")
    if subtitle: st.markdown(f"<p class='small'>{subtitle}</p>", unsafe_allow_html=True)

def show_analysis(result):
    st.session_state.latest_analysis = result.model_dump()
    level = result.risk_level
    css = "danger" if level == "HIGH" else ("warning" if level == "CAUTION" else "safe")
    label = {"HIGH":"HIGH RISK INDICATORS","CAUTION":"CAUTION — VERIFY FIRST","LOW":"NO OBVIOUS INDICATORS FOUND"}[level]
    st.markdown(f"<div class='{css}'><b>{label}</b><br>{result.explanation}</div>", unsafe_allow_html=True)
    st.markdown("**What we noticed**")
    if result.indicators:
        for item in result.indicators: st.markdown(f"- {item}")
    else: st.write("No configured warning patterns were detected. This does not mean the message is genuine.")
    st.markdown("**What to do now**")
    for item in result.recommended_actions: st.markdown(f"- {item}")
    st.markdown("**Never do this**")
    for item in result.never_do: st.markdown(f"- {item}")
    st.caption(result.confidence_note)

def voice_controls(prompt_text=None):
    if not api_key:
        st.info("Voice features need your Gnani API key. Text analysis and demo mode work without it.")
        return
    if not tts_ok:
        st.warning("TTS is unavailable: " + sdk_message)
        return
    text_to_say = prompt_text or ""
    if text_to_say and st.button("🔊 Listen to response", key="tts_"+str(abs(hash(text_to_say)))):
        try:
            audio, error = synthesize_speech(text_to_say, lang_code, api_key)
            if error: st.error(error)
            elif audio: st.audio(audio, format="audio/wav")
        except Exception as exc: st.error(f"Speech generation failed: {exc}")

def audio_input_widget(key):
    audio = st.audio_input("Record your message", key=key)
    if audio:
        if st.button("Transcribe recording", key="transcribe_"+key):
            if not api_key: st.warning("Add GNANI_API_KEY to enable speech-to-text.")
            elif not stt_ok: st.error("STT unavailable: "+sdk_message)
            elif audio.size == 0: st.error("The recording is empty. Please record again.")
            else:
                with st.spinner("Transcribing with Gnani Prisma…"):
                    transcript, error = transcribe_audio(audio.getvalue(), lang_code, api_key, audio.name or "recording.wav")
                if error: st.error(error)
                elif transcript: st.session_state["transcript_"+key] = transcript
                else: st.warning("No speech was detected. Try recording again.")

st.markdown("<div class='hero'><h1>🛡️ PAYPROOF AI</h1><p><b>Think Before You Trust.</b></p><p>Your voice-powered digital payment safety companion.</p></div>", unsafe_allow_html=True)
st.write("")

if page == "Home":
    st.markdown("## Welcome to PayProof AI")
    st.write("Before accepting a payment, verify it safely.")
    c1,c2,c3 = st.columns(3)
    with c1:
        st.markdown("<div class='panel'><h3>💬 Check a message</h3><p>Spot common payment scam warning signs in SMS and chat messages.</p></div>", unsafe_allow_html=True)
        if st.button("Analyse a message →", key="home_msg", use_container_width=True): st.session_state.goto = "Check a Payment Message"; st.rerun()
    with c2:
        st.markdown("<div class='panel'><h3>🧾 Inspect a screenshot</h3><p>Review visible details and missing information. No authenticity claims.</p></div>", unsafe_allow_html=True)
        if st.button("Inspect screenshot →", key="home_img", use_container_width=True): st.session_state.goto = "Inspect Payment Screenshot"; st.rerun()
    with c3:
        st.markdown("<div class='panel'><h3>🎙️ Talk to PayProof</h3><p>Ask practical questions about digital payment safety.</p></div>", unsafe_allow_html=True)
        if st.button("Ask PayProof →", key="home_chat", use_container_width=True): st.session_state.goto = "Ask PayProof"; st.rerun()
    if "goto" in st.session_state:
        target = st.session_state.pop("goto")
        st.info(f"Choose **{target}** from the navigation sidebar.")
    st.markdown("<div class='warning'><b>Payment safety reminder</b><br>Money received? Check your actual bank balance or official payment app before handing over goods. A screenshot or SMS is not proof of credit.</div>", unsafe_allow_html=True)
    st.write("")
    a,b,c = st.columns(3)
    a.metric("Languages", "6", "Malayalam-first")
    b.metric("Analysis", "Explainable", "Rule-based indicators")
    c.metric("Bank verification", "Not connected", "Never claims confirmation")
    st.markdown("### Try a simulated demo")
    demo_names = list(DEMO_SCENARIOS)
    chosen = st.selectbox("Choose a scenario", demo_names)
    demo = DEMO_SCENARIOS[chosen]
    st.markdown(f"<div class='panel'><b>Example input</b><br>{demo['input']}</div>", unsafe_allow_html=True)
    st.markdown("**Expected warning indicators**")
    for x in demo["indicators"]: st.write("• "+x)
    st.markdown("**Suggested response**")
    st.write(demo["response"])
    st.caption("Simulated example — not a real transaction or a finding about a real person.")

elif page == "Check a Payment Message":
    section_header("Check a Payment Message", "Paste a UPI SMS, bank message, payment link or customer chat.")
    audio_input_widget("message")
    text = st.text_area("Message to check", value=st.session_state.get("transcript_message",""), height=150, placeholder="Paste the complete message here…")
    if st.button("Analyse message", type="primary", use_container_width=True):
        if not text.strip(): st.warning("Enter or transcribe a message first.")
        else:
            result = analyze_message(text, lang_name)
            show_analysis(result)
            st.session_state.last_response = result.explanation + " " + " ".join(result.recommended_actions)
    if st.session_state.get("latest_analysis"):
        st.divider()
        st.caption("Latest analysis is an indicator-based assessment, not proof of fraud.")
        voice_controls(st.session_state.get("last_response"))

elif page == "Inspect Payment Screenshot":
    section_header("Payment Screenshot Inspector", "Review visible information and gaps — this tool cannot authenticate an image.")
    st.markdown("<div class='warning'><b>Privacy first:</b> Blur names, phone numbers, UPI IDs, account details and other personal information before uploading. Never upload OTPs, PINs or passwords.</div>", unsafe_allow_html=True)
    upload = st.file_uploader("Upload JPG, JPEG or PNG", type=["jpg","jpeg","png"])
    manual = st.text_area("Optional: describe what the screenshot says", placeholder="Example: It says payment successful for ₹500, but my bank balance has not changed.")
    if upload:
        if upload.size > 8*1024*1024: st.error("Image is larger than the 8 MB limit.")
        else:
            try:
                image = Image.open(upload)
                if image.format not in ("JPEG","PNG"): st.error("Unsupported image format.")
                else:
                    st.image(image, caption="Uploaded image — inspect the visible details carefully.", use_container_width=True)
                    if st.button("Inspect screenshot", type="primary"):
                        report = inspect_image(upload.getvalue(), image.format, manual)
                        st.markdown("<div class='danger'><b>A screenshot is not proof of payment.</b><br>Verify the credit directly in your bank account or official payment application.</div>", unsafe_allow_html=True)
                        st.markdown("**Visible details extracted (if OCR is available)**")
                        st.write(report["extracted_text"] or "No text extracted.")
                        st.markdown("**Review observations**")
                        for item in report["observations"]: st.write("• "+item)
                        if report["ocr_note"]: st.info(report["ocr_note"])
                        st.caption("This is a visual checklist only. No image authenticity or transaction verification is performed.")
            except Exception as exc: st.error(f"Could not read this image: {exc}")
    if manual.strip() and not upload:
        st.info("Your description can be reviewed without uploading an image.")
        if st.button("Review my description"):
            result = analyze_message(manual, lang_name)
            show_analysis(result)

elif page == "Ask PayProof":
    section_header("Ask PayProof", "Ask in your selected language. Responses use a local safety knowledge base unless a documented model endpoint is configured.")
    audio_input_widget("chat")
    for item in st.session_state.messages:
        with st.chat_message(item["role"]): st.write(item["content"])
    question = st.chat_input("Ask about a payment or suspicious request…")
    typed = question or st.session_state.get("transcript_chat","")
    if typed:
        st.session_state["transcript_chat"] = ""
        st.session_state.messages.append({"role":"user","content":typed})
        response = answer_question(typed, lang_name, st.session_state.messages[:-1])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.session_state.last_response = response
        st.rerun()
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":
        voice_controls(st.session_state.messages[-1]["content"])

elif page == "Safety Guide":
    section_header("Safety Guide", "Short lessons for safer digital payments.")
    for lesson in safety_lessons(lang_name):
        with st.expander(lesson["title"], expanded=False):
            st.write("**Why it matters:** "+lesson["why"])
            st.write("**Example:** "+lesson["example"])
            st.success("**Do:** "+lesson["do"])
            st.error("**Avoid:** "+lesson["avoid"])
    st.markdown("<div class='danger'><b>Suspect cyber financial fraud in India?</b><br>Contact the national cybercrime helpline <b>1930</b> promptly or use the official <a href='https://cybercrime.gov.in/' target='_blank'>National Cyber Crime Reporting Portal</a>. Use official channels; do not trust numbers or links sent by the suspicious caller.</div>", unsafe_allow_html=True)

elif page == "About":
    section_header("About PayProof AI")
    st.markdown("""
    <div class='panel'>
    <h3>Think Before You Trust.</h3>
    PayProof AI is a multilingual, voice-first payment safety companion for small merchants and everyday users.
    It helps explain warning signs in messages, review visible screenshot details and learn safe verification habits.
    <br><br><b>Important boundary:</b> PayProof AI has no bank or UPI-provider connection. It cannot confirm whether funds have arrived, authenticate screenshots, or determine fraud with certainty.
    </div>""", unsafe_allow_html=True)
    st.write("**Technology:** Streamlit · Python · Pydantic · Pillow · Gnani Prisma STT · Gnani Timbre TTS")
    st.write("**Voice status:** "+("API key configured" if api_key else "Demo mode — add GNANI_API_KEY to enable speech services"))
    st.write("**SDK status:** "+sdk_message)
    st.caption("No uploaded screenshot is saved by this app. Audio is processed through a temporary file that is deleted after transcription. Voice recordings are sent to the configured speech provider when you request transcription.")

st.markdown("---")
st.caption("PayProof AI is an educational safety assistant, not a bank, payment provider, fraud investigation service or legal authority. Always verify credits independently.")
