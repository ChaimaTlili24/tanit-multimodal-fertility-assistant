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
    Returns an empty string if there is nothing to transcribe.
    """
    if audio_path is None:
        return ""

    model = get_whisper_model()

    segments, info = model.transcribe(audio_path, beam_size=5)
    text = "".join(segment.text for segment in segments).strip()

    return text
