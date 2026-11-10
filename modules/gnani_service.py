
import os
import streamlit as st


def get_api_key():
    try:
        value = st.secrets.get("GNANI_API_KEY", "")
        if value:
            return str(value).strip()
    except Exception:
        pass

    return os.getenv("GNANI_API_KEY", "").strip()


@st.cache_resource(show_spinner=False)
def get_clients(api_key):
    from gnani.stt import GnaniSTTClient
    from gnani.tts import GnaniTTSClient

    stt_client = GnaniSTTClient(api_key=api_key)
    tts_client = GnaniTTSClient(api_key=api_key)

    return stt_client, tts_client


def sdk_status():
    stt_available = False
    tts_available = False
    errors = []

    try:
        from gnani.stt import GnaniSTTClient
        stt_available = True
    except Exception as exc:
        errors.append(
            f"STT: {type(exc).__name__}: {exc}"
        )

    try:
        from gnani.tts import GnaniTTSClient, AudioConfig
        tts_available = True
    except Exception as exc:
        errors.append(
            f"TTS: {type(exc).__name__}: {exc}"
        )

    if stt_available and tts_available:
        message = "Gnani STT and TTS imports are available."
    elif stt_available:
        message = "STT is available, but TTS is unavailable. " + "; ".join(errors)
    elif tts_available:
        message = "TTS is available, but STT is unavailable. " + "; ".join(errors)
    else:
        message = "Gnani SDK imports failed. " + "; ".join(errors)

    return stt_available, tts_available, message
