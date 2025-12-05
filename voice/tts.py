from typing import Optional


def synthesize_speech(text: str, lang: str = "fr") -> Optional[str]:
    """
    Text-To-Speech (TTS) stub.

    - For now, this function does not generate any real audio.
    - It simply returns None.
    - Later, it can be replaced by a real implementation
      (gTTS, Coqui TTS, pyttsx3, etc.) and return the path
      to the generated audio file.

    Args:
        text: text to be spoken.
        lang: target language code (e.g., "fr", "en").

    Returns:
        Path to the generated audio file, or None if nothing is done.
    """
    if not text or not text.strip():
        return None

    # TODO: implement real TTS here if needed.
    # Example (future):
    #   - generate an .mp3 in a temporary file
    #   - return the file path so Gradio can play it

    return None
