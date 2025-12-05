"""
RAG simple (stub) pour le prototype Tanit Multimodal Fertility Assistant.

Pour l'instant :
- on ne charge pas encore de vrais documents,
- on ne fait pas encore de vraie similarité sémantique.

Mais :
- l'interface `retrieve_context(question: str) -> str` est déjà prête,
- on pourra brancher plus tard un vrai index vectoriel ou GraphRAG
  sans toucher au reste de l'application.
"""


from typing import Optional


def retrieve_context(question: str) -> str:
    """
    Retourne un contexte textuel basé sur la question.

    Version actuelle : stub "intelligent" très simple.
    Version future   : utiliser un index (FAISS, LlamaIndex, GraphRAG, etc.)
    sur des PDF/guidelines de fertilité.
    """

    question_lower = (question or "").lower()

    if any(word in question_lower for word in ["amh", "réserve", "reserve", "ovaire", "ovarienne"]):
        return (
            "Contexte (simulé) : L'AMH est un marqueur de la réserve ovarienne. "
            "Une valeur basse suggère un stock d'ovocytes plus limité, "
            "mais ne prédit pas à elle seule la capacité à concevoir. "
            "Les recommandations médicales insistent sur l'interprétation globale "
            "avec l'âge, l'historique des cycles et d'autres hormones."
        )

    if "pcos" in question_lower or "sopk" in question_lower:
        return (
            "Contexte (simulé) : Le SOPK (PCOS) est un syndrome fréquent associé à des "
            "cycles irréguliers, parfois une résistance à l'insuline et une augmentation "
            "du nombre de follicules visibles à l'échographie. "
            "La fertilité peut être impactée mais beaucoup de patientes conçoivent avec "
            "un suivi adapté et des ajustements de mode de vie ou traitement."
        )

    if "âge" in question_lower or "age" in question_lower or "ans" in question_lower:
        return (
            "Contexte (simulé) : L'âge est un facteur majeur de la fertilité. "
            "La réserve ovarienne et la qualité ovocytaire diminuent en moyenne après 35 ans, "
            "mais il existe de grandes variations individuelles. "
            "Les décisions médicales se basent sur l'ensemble du profil clinique."
        )

    # fallback très général
    return (
        "Contexte (simulé) : En fertilité, l'interprétation des résultats se fait toujours "
        "dans un cadre global (âge, antécédents, hormones, échographies, symptômes). "
        "Aucun chiffre isolé ne suffit pour conclure. Les recommandations encouragent "
        "une discussion personnalisée avec un spécialiste."
    )
