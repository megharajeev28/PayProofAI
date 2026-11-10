
import os
import tempfile
import streamlit as st


def _transcript_text(result):
    """Extract transcript from common SDK response formats."""

    if isinstance(result, str):
        return result.strip()

    if isinstance(result, dict):
        for key in ("text", "transcript", "transcription", "utterance"):
            value = result.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

        for key in ("data", "result"):
            nested = result.get(key)
            if nested is not None:
                text = _transcript_text(nested)
                if text:
                    return text

    for key in ("text", "transcript", "transcription"):
        value = getattr(result, key, None)
        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


@st.cache_resource(show_spinner=False)
def get_stt_client(api_key):
    from gnani.stt import GnaniSTTClient
    return GnaniSTTClient(api_key=api_key)


@st.cache_resource(show_spinner=False)
def get_tts_client(api_key):
    from gnani.tts import GnaniTTSClient
    return GnaniTTSClient(api_key=api_key)


def transcribe_audio(
    audio_bytes,
    language_code,
    api_key,
    filename="recording.wav"
):
    if not api_key:
        return "", "Gnani API key is missing."

    if not audio_bytes:
        return "", "The recording is empty."

    suffix = os.path.splitext(filename)[1].lower()

    supported = (".wav", ".mp3", ".m4a", ".webm", ".ogg")

    if suffix not in supported:
        return "", "Unsupported audio format: " + suffix

    if len(audio_bytes) < 100:
        return "", "Audio recording is too small. Please record again."

    path = None

    try:
        stt = get_stt_client(api_key)

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as tmp:
            tmp.write(audio_bytes)
            path = tmp.name

        result = stt.transcribe(
            path,
            language_code=language_code
        )

        transcript = _transcript_text(result)

        if not transcript:
            return "", "No transcript returned. Try recording again."

        return transcript, None

    except Exception as exc:
        return "", (
            f"Transcription failed "
            f"({type(exc).__name__}): {exc}"
        )

    finally:
        if path and os.path.exists(path):
            try:
                os.remove(path)
            except OSError:
                pass


def synthesize_speech(text, language_code, api_key):
    if not api_key:
        return None, "Gnani API key is missing."

    if not text or not text.strip():
        return None, "There is no response text to speak."

    try:
        from gnani.tts import AudioConfig

        tts = get_tts_client(api_key)

        speech = tts.synthesize(
            text.strip(),
            voice="Nalini",
            model="timbre-v2.5",
            language=language_code,
            speed=1.0,
            audio_config=AudioConfig(
                sample_rate=16000,
                encoding="linear_pcm",
                container="wav"
            )
        )

        if isinstance(speech, dict):
            speech = (
                speech.get("audio")
                or speech.get("audio_data")
                or speech.get("data")
            )

        if hasattr(speech, "content"):
            speech = speech.content

        if not isinstance(speech, (bytes, bytearray)):
            return None, "TTS returned an unsupported audio format."

        if not speech:
            return None, "TTS returned empty audio."

        return bytes(speech), None

    except Exception as exc:
        return None, (
            f"Speech generation failed "
            f"({type(exc).__name__}): {exc}"
        )
