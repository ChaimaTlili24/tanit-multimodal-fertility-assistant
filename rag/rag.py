"""
Simple RAG stub for the Tanit Multimodal Fertility Assistant prototype.

For now:
- we do NOT load any real documents,
- we do NOT compute real semantic similarity.

But:
- the interface `retrieve_context(question: str) -> str` is already stable,
- we can later plug in a real vector index or GraphRAG
  without changing the rest of the application.
"""

from typing import Optional


def retrieve_context(question: str) -> str:
    """
    Return a textual context snippet based on the user question.

    Current version: a very simple "smart" stub using keyword checks.
    Future version: use a real index (FAISS, LlamaIndex, GraphRAG, etc.)
    on fertility PDFs / clinical guidelines.
    """

    question_lower = (question or "").lower()

    # AMH / ovarian reserve
    if any(word in question_lower for word in ["amh", "reserve", "réserve", "ovary", "ovarian", "ovarienne"]):
        return (
            "Simulated context: Anti-Müllerian hormone (AMH) is a marker of ovarian reserve. "
            "Lower AMH values suggest a smaller remaining pool of eggs, but AMH alone does not "
            "determine whether someone can conceive. Medical guidelines emphasise interpreting "
            "AMH together with age, cycle history, ultrasound findings and other hormones."
        )

    # PCOS / SOPK
    if "pcos" in question_lower or "sopk" in question_lower:
        return (
            "Simulated context: Polycystic Ovary Syndrome (PCOS) is a common condition often "
            "associated with irregular cycles, possible insulin resistance and an increased number "
            "of small follicles on ultrasound. Fertility can be affected, but many patients with PCOS "
            "do conceive with appropriate lifestyle measures and medical follow-up when needed."
        )

    # Age / years
    if "âge" in question_lower or "age" in question_lower or "ans" in question_lower or "years" in question_lower:
        return (
            "Simulated context: Age is a major factor in fertility. On average, ovarian reserve and egg "
            "quality decline after around 35 years old, but there is large individual variation. "
            "Clinical decisions always take into account the full picture, not age alone."
        )

    # Very general fallback
    return (
        "Simulated context: In fertility, results are always interpreted in a global context "
        "(age, medical history, hormones, ultrasound findings, symptoms). A single number on its "
        "own is not enough to reach a conclusion. Current recommendations encourage a personalised "
        "discussion with a fertility specialist."
    )
