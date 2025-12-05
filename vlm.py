"""
vlm.py – Utilitaires pour le modèle Vision-Language (VLM)

Objectif :
- Analyser des images médicales (bilans, courbes, échographies, rapports scannés)
- Retourner un résumé textuel exploitable par le LLM / RAG.

Pour l'instant :
- On reste en mode "stub" (texte simulé),
- Mais la structure est prête pour brancher un vrai VLM (ex: Qwen3-VL-4B-Instruct).

Tu pourras plus tard :
- activer USE_REAL_VLM = True,
- ajouter le code de chargement du modèle HuggingFace dans `load_vlm_model()`,
- et implémenter la partie réelle dans `analyze_image_with_vlm()`.
"""

from typing import Optional

# Toggle pour activer/désactiver le vrai VLM plus tard.
USE_REAL_VLM = False


# ==============================
#     CHARGEMENT DU VLM
# ==============================

_vlm_model = None
_vlm_processor = None


def load_vlm_model():
    """
    Charge le modèle VLM en mémoire (à implémenter plus tard).

    Exemple futur (pseudo-code) :

        from transformers import AutoModelForVision2Seq, AutoProcessor

        model_name = "chemin/vers/qwen3-vl-4b-instruct"
        model = AutoModelForVision2Seq.from_pretrained(model_name)
        processor = AutoProcessor.from_pretrained(model_name)

        return model, processor
    """
    global _vlm_model, _vlm_processor

    if _vlm_model is not None and _vlm_processor is not None:
        return _vlm_model, _vlm_processor

    # TODO : implémenter le chargement réel du modèle VLM ici.
    # Pour l'instant, on laisse comme None.
    _vlm_model, _vlm_processor = None, None
    return _vlm_model, _vlm_processor


# ==============================
#     ANALYSE D'IMAGE
# ==============================

def _analyze_image_stub(image_path: str, user_question: str) -> str:
    """
    Version stub : retourne un résumé simulé.
    Utilisée tant que USE_REAL_VLM = False.
    """
    return (
        "Analyse (simulée) de l'image :\n"
        "- Lecture approximative du document ou de l'examen.\n"
        "- Extraction des valeurs hormonales ou des éléments clés.\n"
        "- Ce texte est uniquement un placeholder, le vrai VLM "
        "sera branché dans une version ultérieure."
    )


def analyze_image_with_vlm(image_path: str, user_question: str) -> str:
    """
    Version future : utiliser un vrai VLM pour analyser l'image.
    Pour l'instant, non implémentée.
    """
    model, processor = load_vlm_model()
    if model is None or processor is None:
        # Sécurité : si le modèle n'est pas disponible, on renvoie le stub
        return _analyze_image_stub(image_path, user_question)

    # TODO : implémenter l'appel réel au VLM ici.
    # Exemple futur (pseudo-code) :
    #
    #   inputs = processor(images=image, text=user_question, return_tensors="pt")
    #   outputs = model.generate(**inputs)
    #   answer = processor.batch_decode(outputs, skip_special_tokens=True)[0]
    #
    #   return answer
    #
    return _analyze_image_stub(image_path, user_question)


def analyze_image(image_path: Optional[str], user_question: str) -> str:
    """
    Point d'entrée utilisé par l'application.
    - Si aucune image : retourne une chaîne vide.
    - Si USE_REAL_VLM = False : utilise le stub.
    - Sinon : utilise le vrai VLM.
    """
    if image_path is None:
        return ""

    if not USE_REAL_VLM:
        return _analyze_image_stub(image_path, user_question)

    return analyze_image_with_vlm(image_path, user_question)


# ==============================
#     ANALYSE DE PDF (BASIQUE)
# ==============================

def analyze_pdf(pdf_path: Optional[str], user_question: str) -> str:
    """
    Pour l'instant :
    - stub simple : renvoie un texte générique.
    - plus tard : extraction des pages importantes, éventuellement conversion
      en images et envoi au VLM page par page.
    """
    if pdf_path is None:
        return ""

    return (
        "Analyse (simulée) du PDF : le document semble contenir un rapport ou "
        "un bilan médical. Dans une version ultérieure, le système extraira "
        "les pages pertinentes (bilans hormonaux, échographies, recommandations) "
        "et les analysera avec le VLM."
    )
