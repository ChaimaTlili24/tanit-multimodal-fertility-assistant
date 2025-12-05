from typing import Optional


def synthesize_speech(text: str, lang: str = "fr") -> Optional[str]:
    """
    Stub TTS (Text-To-Speech).

    - Pour l'instant, cette fonction ne génère pas encore d'audio réel.
    - Elle retourne simplement None.
    - Plus tard, on pourra la remplacer par une vraie implémentation
      (gTTS, Coqui TTS, pyttsx3, etc.) et faire retourner le chemin du
      fichier audio généré.

    Args:
        text: texte à lire
        lang: langue cible (ex: 'fr', 'en')

    Returns:
        Chemin du fichier audio généré, ou None si rien n'est fait.
    """
    if not text or not text.strip():
        return None

    # TODO: implémenter une vraie synthèse vocale ici si besoin.
    # Exemple futur:
    #   - générer un .mp3 dans un fichier temporaire
    #   - retourner le chemin de ce fichier pour que Gradio l'affiche

    return None
