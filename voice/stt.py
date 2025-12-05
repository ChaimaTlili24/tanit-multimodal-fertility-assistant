from typing import Optional
from functools import lru_cache
from faster_whisper import WhisperModel


@lru_cache(maxsize=1)
def get_whisper_model() -> WhisperModel:
    """
    Charge le modèle faster-whisper une seule fois (singleton).
    Tu peux changer 'medium' en 'small' ou 'large-v3' selon les ressources.
    """
    # device="cpu" pour être sûr que ça tourne partout
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    return model


def transcribe_audio(audio_path: Optional[str]) -> str:
    """
    Transcrit un fichier audio en texte avec faster-whisper.
    Retourne une string vide si rien à transcrire.
    """
    if audio_path is None:
        return ""

    model = get_whisper_model()

    segments, info = model.transcribe(audio_path, beam_size=5)
    text = "".join(segment.text for segment in segments).strip()

    return text
