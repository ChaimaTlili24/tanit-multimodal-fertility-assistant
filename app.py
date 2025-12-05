import gradio as gr
from typing import List, Dict, Any, Optional
from pathlib import Path

from voice.stt import transcribe_audio
from rag.rag import retrieve_context
from vlm import analyze_image, analyze_pdf

# Load CSS from assets/style.css
CSS_PATH = Path(__file__).parent / "assets" / "style.css"
custom_css = CSS_PATH.read_text(encoding="utf-8")


# ==============================
#  BACKEND WRAPPERS / STUBS
# ==============================

def simple_stt_transcribe(audio_path: Optional[str]) -> str:
    """
    Wrapper around the real faster-whisper STT model defined in voice/stt.py.
    """
    if audio_path is None:
        return ""
    return transcribe_audio(audio_path)


def simple_image_analysis(image_path: Optional[str], user_text: str) -> str:
    """
    Wrapper around vlm.analyze_image().
    """
    return analyze_image(image_path, user_text or "")


def simple_pdf_analysis(pdf_path: Optional[str], user_text: str) -> str:
    """
    Wrapper around vlm.analyze_pdf().
    """
    return analyze_pdf(pdf_path, user_text or "")


def simple_rag_answer(user_text: str, extra_context: str) -> str:
    """
    Combine:
    - RAG context (using the text if available, otherwise multimodal context),
    - multimodal context (voice / image / PDF),
    - and format a final, safety-aware response.
    """
    base_disclaimer = (
        "⚕️ *I am an educational fertility assistant and do not replace a doctor.*\n"
        "For any medical decision or treatment, please always consult a qualified healthcare professional.\n\n"
    )

    # If the user did not type any text, try to use the multimodal context
    rag_input = (user_text or "").strip()
    if not rag_input and extra_context:
        rag_input = extra_context

    # Simple RAG context (stub for now)
    rag_context = retrieve_context(rag_input or "")

    # Text shown in "Your question:"
    if user_text and user_text.strip():
        question_block = f"**Your question:** {user_text}"
    elif extra_context:
        question_block = (
            "**Your question:** [no text, but you sent a document; "
            "I am basing my explanation on its content and medical context.]"
        )
    else:
        question_block = "**Your question:** [no content received]"

    response = (
        f"{base_disclaimer}"
        f"**Medical context (RAG):** {rag_context}\n\n"
        f"{question_block}\n\n"
        f"**Multimodal context (audio / image / PDF):** {extra_context or '[none]'}\n\n"
        "💡 *This answer is a general educational explanation. "
        "It does not replace an individual medical consultation.*"
    )

    return response


# ==============================
#  CHATBOT LOGIC
# ==============================

def chat_pipeline(
    history: List[Dict[str, Any]],
    user_text: str,
    user_audio,
    user_image,
    user_pdf,
):
    """
    Main function called by Gradio for each user interaction.

    Args:
        history: list of messages in the form [{"role": "...", "content": "..."}, ...]
        user_text: text typed by the user
        user_audio: audio file path (or None)
        user_image: image file path (or None)
        user_pdf: PDF file path (or None)
    """

    # 1) Audio transcription (real STT)
    transcribed = simple_stt_transcribe(user_audio)

    # 2) Image analysis (VLM stub for now)
    image_summary = simple_image_analysis(user_image, user_text)

    # 3) PDF analysis (stub)
    pdf_summary = simple_pdf_analysis(user_pdf, user_text)

    # 4) Build additional multimodal context
    extra_parts = []
    if transcribed:
        extra_parts.append(f"Voice: {transcribed}")
    if image_summary:
        extra_parts.append(f"Image: {image_summary}")
    if pdf_summary:
        extra_parts.append(f"PDF: {pdf_summary}")

    extra_context = " | ".join(extra_parts)

    # 5) Final user text = typed text + transcription if present
    full_user_text = user_text or ""
    if transcribed:
        full_user_text += f"\n\n[+ Voice transcription]: {transcribed}"

    # 6) Generate the assistant answer (RAG + LLM stub)
    assistant_message = simple_rag_answer(full_user_text, extra_context)

    # 7) Update history in "messages" format
    if full_user_text.strip():
        history.append({"role": "user", "content": full_user_text})

    history.append({"role": "assistant", "content": assistant_message})

    # Return:
    # - updated history for the Chatbot
    # - cleared text
    # - reset audio
    # - reset image
    # - reset PDF
    return history, "", None, None, None


# ==============================
#  GRADIO INTERFACE
# ==============================

def build_interface():
    with gr.Blocks(
        title="Tanit Multimodal Fertility Assistant",
    ) as demo:

        # === Optional: existing external CSS (keep if you still use assets/style.css) ===
        gr.Markdown(f"<style>{custom_css}</style>", visible=True)

        # === Palette applied directly here (same as logo) ===
        palette_css = """
        body {
            background-color: #f5f2fb;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }

        /* Header row */
        #tanit-header-row {
            background: linear-gradient(90deg, #6a4bbf, #4e3795);
            color: #ffffff;
            padding: 18px 24px;
            border-radius: 14px;
            margin-bottom: 18px;
            display: flex;
            align-items: center;
        }

        #tanit-header-row .tanit-logo img {
            max-height: 64px;
        }

        .tanit-title-main {
            font-size: 20px;
            font-weight: 650;
        }
        .tanit-title-sub {
            font-size: 13px;
            opacity: 0.9;
        }
        .tanit-title-tagline {
            font-size: 12px;
            opacity: 0.85;
            margin-top: 4px;
        }

        /* Main columns as cards */
        .tanit-main-row > .tanit-chat-column,
        .tanit-main-row > .tanit-input-column {
            background: #ffffff;
            border-radius: 14px;
            box-shadow: 0 10px 24px rgba(0, 0, 0, 0.04);
            padding: 14px;
        }

        /* Chatbot box */
        .tanit-chatbot {
            border-radius: 12px !important;
            border: 1px solid #e3ddf7;
        }

        /* Primary and secondary buttons */
        #submit-btn,
        .tanit-primary-btn {
            background: #6a4bbf !important;
            border-color: #6a4bbf !important;
            color: #ffffff !important;
        }
        #submit-btn:hover,
        .tanit-primary-btn:hover {
            background: #5536a0 !important;
            border-color: #5536a0 !important;
        }

        #clear-btn,
        .tanit-secondary-btn {
            background: #ffffff !important;
            border-color: #6a4bbf !important;
            color: #6a4bbf !important;
        }
        #clear-btn:hover,
        .tanit-secondary-btn:hover {
            background: #f0eafd !important;
        }

        /* Small accent (teal from logo) for audio/image/file labels */
        .tanit-input-column label {
            color: #22c2b5;
            font-weight: 500;
        }
        """
        gr.Markdown(f"<style>{palette_css}</style>")

        # === Tanit.ai branding header ===
        with gr.Row(elem_id="tanit-header-row"):
            with gr.Column(scale=1):
                gr.Image(
                    value="assets/logo.png",   # logo path
                    show_label=False,
                    interactive=False,
                    container=False,
                    elem_classes="tanit-logo",
                )
            with gr.Column(scale=5):
                gr.Markdown(
                    """
                    <div class="tanit-title-main">Tanit.ai – Fertility Companion</div>
                    <div class="tanit-title-sub">Your personal companion towards parenthood.</div>
                    <div class="tanit-title-tagline">
                        Multimodal assistant (text · voice · documents) to support patients
                        in their fertility journey, with a warm and medically cautious tone.
                    </div>
                    """,
                )

        # === Medical disclaimer ===
        gr.Markdown(
            """
            > ⚠️ **Disclaimer:** This prototype is strictly educational.  
            > It does not replace professional medical advice, diagnosis, or prescription.
            """
        )

        # === Main layout: chat on the left, inputs on the right ===
        with gr.Row(elem_classes="tanit-main-row"):
            # Left column: chatbot
            with gr.Column(scale=3, elem_classes="tanit-chat-column"):
                chatbot = gr.Chatbot(
                    label="Conversation",
                    height=500,
                    elem_classes="tanit-chatbot",
                )

            # Right column: user inputs
            with gr.Column(scale=1, elem_classes="tanit-input-column"):
                gr.Markdown("### User input")

                text_input = gr.Textbox(
                    label="Text message",
                    placeholder="Describe your situation, test results, and questions...",
                    lines=4,
                )

                audio_input = gr.Audio(
                    label="Voice (microphone)",
                    sources=["microphone"],
                    type="filepath",
                )

                image_input = gr.Image(
                    label="Medical image (hormone panel, chart, ultrasound...)",
                    type="filepath",
                )

                pdf_input = gr.File(
                    label="Report / analysis (PDF)",
                    file_types=[".pdf"],
                )

                submit_btn = gr.Button(
                    "Send",
                    elem_id="submit-btn",
                    elem_classes="tanit-primary-btn",
                )
                clear_btn = gr.Button(
                    "Clear conversation",
                    elem_id="clear-btn",
                    elem_classes="tanit-secondary-btn",
                )

        # === Send button ===
        submit_btn.click(
            fn=chat_pipeline,
            inputs=[chatbot, text_input, audio_input, image_input, pdf_input],
            outputs=[chatbot, text_input, audio_input, image_input, pdf_input],
        )

        # === Clear button ===
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
