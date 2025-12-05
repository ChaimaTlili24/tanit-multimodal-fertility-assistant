import gradio as gr
from typing import List, Dict, Any, Optional

from voice.stt import transcribe_audio


# ==============================
#  STUBS / PLACEHOLDERS BACKEND
# ==============================

def simple_stt_transcribe(audio_path: Optional[str]) -> str:
    """
    Wrapper qui utilise le vrai modèle faster-whisper défini dans voice/stt.py.
    """
    if audio_path is None:
        return ""
    return transcribe_audio(audio_path)


def simple_image_analysis(image_path: Optional[str]) -> str:
    """
    Stub temporaire pour l'analyse d'image.
    Plus tard : remplacé par Qwen3-VL-4B-Instruct (VLM).
    """
    if image_path is None:
        return ""
    return "[Résumé simulé de l'image médicale]"


def simple_pdf_analysis(pdf_path: Optional[str]) -> str:
    """
    Stub temporaire pour l'analyse de PDF.
    Plus tard : extraction pages + VLM ou RAG dessus.
    """
    if pdf_path is None:
        return ""
    return "[Résumé simulé du PDF médical]"


def simple_rag_answer(user_text: str, extra_context: str) -> str:
    """
    Stub temporaire pour le RAG + LLM.
    Plus tard : remplacé par (GraphRAG ou RAG vectoriel) + Qwen3-4B-Instruct.
    """
    base_disclaimer = (
        "⚕️ *Je suis un assistant éducatif sur la fertilité et je ne remplace pas un médecin.*\n"
        "Pour toute décision médicale ou traitement, consulte toujours un professionnel de santé.\n\n"
    )

    response = (
        "Merci pour ta question. Voici une réponse simulée (le back-end RAG/LLM "
        "n'est pas encore branché) :\n\n"
        f"**Ta question :** {user_text or '[vide]'}\n\n"
        f"**Contexte reçu (audio/image/PDF) :** {extra_context or '[aucun]'}"
    )

    return base_disclaimer + response


# ==============================
#  LOGIQUE CHATBOT
# ==============================

def chat_pipeline(
    history: List[Dict[str, Any]],
    user_text: str,
    user_audio,
    user_image,
    user_pdf,
):
    """
    Fonction centrale appelée par Gradio à chaque message.

    - history : liste de messages au format [{"role": "...", "content": "..."}, ...]
    - user_text : texte tapé
    - user_audio : fichier audio (chemin) ou None
    - user_image : image (chemin) ou None
    - user_pdf : PDF (chemin) ou None
    """

    # 1) Transcription audio (STT réel)
    transcribed = simple_stt_transcribe(user_audio)

    # 2) Analyse image (stub)
    image_summary = simple_image_analysis(user_image)

    # 3) Analyse PDF (stub)
    pdf_summary = simple_pdf_analysis(user_pdf)

    # 4) Contexte supplémentaire
    extra_parts = []
    if transcribed:
        extra_parts.append(f"Voix: {transcribed}")
    if image_summary:
        extra_parts.append(f"Image: {image_summary}")
    if pdf_summary:
        extra_parts.append(f"PDF: {pdf_summary}")

    extra_context = " | ".join(extra_parts)

    # 5) Texte final de l'utilisateur = texte tapé + transcription si présente
    full_user_text = user_text or ""
    if transcribed:
        full_user_text += f"\n\n[+ Transcription voix]: {transcribed}"

    # 6) Génération de la réponse (stub RAG+LLM)
    assistant_message = simple_rag_answer(full_user_text, extra_context)

    # 7) Mise à jour de l'historique au format messages
    if full_user_text.strip():
        history.append({"role": "user", "content": full_user_text})
    else:
        history.append({"role": "user", "content": "[message vide]"})

    history.append({"role": "assistant", "content": assistant_message})

    # On retourne :
    # - l'historique pour le Chatbot
    # - texte vidé
    # - audio reset
    # - image reset
    # - pdf reset
    return history, "", None, None, None


# ==============================
#  INTERFACE GRADIO
# ==============================

def build_interface():
    with gr.Blocks(title="Tanit Multimodal Fertility Assistant") as demo:
        gr.Markdown(
            """
            # 🧬 Tanit Multimodal Fertility Assistant (Prototype)

            Assistant multimodal pour accompagner les patientes en fertilité :
            texte, voix, images médicales et documents.

            > ⚠️ **Attention :** Ce prototype est strictement éducatif.  
            > Il ne remplace en aucun cas un avis médical professionnel.
            """
        )

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=500,
                )

            with gr.Column(scale=1):
                gr.Markdown("### Entrée utilisateur")

                text_input = gr.Textbox(
                    label="Message texte",
                    placeholder="Décris ta situation, tes résultats, tes questions...",
                    lines=4,
                )

                audio_input = gr.Audio(
                    label="Voix (micro)",
                    sources=["microphone"],
                    type="filepath",
                )

                image_input = gr.Image(
                    label="Image médicale (bilan, courbe, échographie...)",
                    type="filepath",
                )

                pdf_input = gr.File(
                    label="Rapport / Analyse au format PDF",
                    file_types=[".pdf"],
                )

                submit_btn = gr.Button("Envoyer")
                clear_btn = gr.Button("Effacer la conversation")

        # Bouton "Envoyer"
        submit_btn.click(
            fn=chat_pipeline,
            inputs=[chatbot, text_input, audio_input, image_input, pdf_input],
            outputs=[chatbot, text_input, audio_input, image_input, pdf_input],
        )

        # Bouton "Effacer"
        def clear_all():
            return [], "", None, None, None

        clear_btn.click(
            fn=clear_all,
            inputs=None,
            outputs=[chatbot, text_input, audio_input, image_input, pdf_input],
        )

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch()
