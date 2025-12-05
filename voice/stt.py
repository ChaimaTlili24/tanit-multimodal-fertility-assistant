from typing import Optional
from functools import lru_cache
from faster_whisper import WhisperModel


@lru_cache(maxsize=1)
def get_whisper_model() -> WhisperModel:
    """
    Load the faster-whisper model only once (singleton pattern).
    You can change 'medium' to 'small' or 'large-v3' depending on resources.
    """
    # device="cpu" to make sure it runs everywhere (Kaggle / local CPU)
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    return model


def transcribe_audio(audio_path: Optional[str]) -> str:
    """
    Transcribe an audio file to text using faster-whisper.

    - First pass: auto language detection.
    - If the detected language is 'en' or 'fr', we keep the result.
    - If the detected language is something else (e.g. 'ar'),
      we fall back to a second pass forcing English transcription.

    Returns:
        Transcribed text (string), or empty string if nothing to transcribe.
    """
    if audio_path is None:
        return ""

    model = get_whisper_model()

    # First pass: auto-detect language
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        task="transcribe",
    )
    detected_lang = info.language
    text = "".join(segment.text for segment in segments).strip()

    # If language is English or French, we keep it as is
    if detected_lang in ("en", "fr"):
        return text

    # Otherwise (e.g. 'ar'), we force English transcription as a fallback
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        task="transcribe",
        language="en",
    )
    text = "".join(segment.text for segment in segments).strip()
    return text
