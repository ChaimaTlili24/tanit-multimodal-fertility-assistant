"""
vlm.py – Utilities for the Vision-Language Model (VLM)

Goal:
- Analyze medical images (hormone panels, cycle charts, ultrasounds, scanned reports)
- Return a textual summary that can be used by the LLM / RAG layer.

For now:
- We stay in "stub" mode (simulated text),
- But the structure is ready to plug in a real VLM (e.g. Qwen3-VL-4B-Instruct).

Later you can:
- set USE_REAL_VLM = True,
- add the HuggingFace model loading code in `load_vlm_model()`,
- and implement the real logic in `analyze_image_with_vlm()`.
"""

from typing import Optional

# Toggle to enable/disable the real VLM in the future.
USE_REAL_VLM = False


# ==============================
#     VLM LOADING
# ==============================

_vlm_model = None
_vlm_processor = None


def load_vlm_model():
    """
    Load the VLM into memory (to be implemented later).

    Future example (pseudo-code):

        from transformers import AutoModelForVision2Seq, AutoProcessor

        model_name = "path/to/qwen3-vl-4b-instruct"
        model = AutoModelForVision2Seq.from_pretrained(model_name)
        processor = AutoProcessor.from_pretrained(model_name)

        return model, processor
    """
    global _vlm_model, _vlm_processor

    if _vlm_model is not None and _vlm_processor is not None:
        return _vlm_model, _vlm_processor

    # TODO: implement real VLM loading here.
    # For now, we just keep them as None.
    _vlm_model, _vlm_processor = None, None
    return _vlm_model, _vlm_processor


# ==============================
#     IMAGE ANALYSIS
# ==============================

def _analyze_image_stub(image_path: str, user_question: str) -> str:
    """
    Stub version: returns a simulated summary.
    Used as long as USE_REAL_VLM = False.
    """
    return (
        "Simulated analysis of the image:\n"
        "- Approximate reading of the document or exam.\n"
        "- Extraction of hormone values or key elements (simulated).\n"
        "- This text is only a placeholder; the real VLM will be connected "
        "in a later version."
    )


def analyze_image_with_vlm(image_path: str, user_question: str) -> str:
    """
    Future version: use a real VLM to analyze the image.
    For now, not implemented.
    """
    model, processor = load_vlm_model()
    if model is None or processor is None:
        # Safety: if the model is not available, fall back to the stub.
        return _analyze_image_stub(image_path, user_question)

    # TODO: implement the real VLM call here.
    # Future example (pseudo-code):
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
    Main entry point used by the application.
    - If no image: returns an empty string.
    - If USE_REAL_VLM = False: uses the stub.
    - Otherwise: uses the real VLM.
    """
    if image_path is None:
        return ""

    if not USE_REAL_VLM:
        return _analyze_image_stub(image_path, user_question)

    return analyze_image_with_vlm(image_path, user_question)


# ==============================
#     BASIC PDF ANALYSIS
# ==============================

def analyze_pdf(pdf_path: Optional[str], user_question: str) -> str:
    """
    For now:
    - simple stub: returns a generic text.
    - later: extract key pages, possibly convert them to images and send them
      to the VLM page by page.
    """
    if pdf_path is None:
        return ""

    return (
        "Simulated analysis of the PDF: the document seems to contain a report "
        "or medical summary. In a later version, the system will extract relevant "
        "pages (hormone panels, ultrasound reports, recommendations) and analyze "
        "them with the VLM."
    )
