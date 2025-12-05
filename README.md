# tanit-multimodal-fertility-assistant

Multimodal fertility companion prototype built for the  
**“Multimodal Gen AI Intern (VLM / LLM / Voice)”** assignment at **Tanit.ai**.

The goal of this project is to explore how a **single-page chatbot** can combine:

- Text chat
- Voice input (speech-to-text)
- Image & PDF upload (hormone panels, cycle charts, ultrasound snapshots, lab reports)
- RAG-style grounding on fertility knowledge (currently stubbed, designed for GraphRAG / vector RAG)

> ⚠️ **Medical disclaimer**  
> This assistant is strictly educational. It does **not** provide medical diagnosis or treatment recommendations and must never replace consultation with a qualified healthcare professional.

---

## 1. Features

- **Single-page Gradio UI**
  - Left: chat conversation with the assistant  
  - Right: input panel (text, microphone, medical image upload, PDF upload)

- **Voice input**
  - Microphone recording  
  - Transcription via `faster-whisper` (or stub, depending on environment)

- **Image & PDF inputs (VLM-ready)**
  - Upload hormone panels, cycle charts, ultrasound snippets, or lab reports
  - Currently processed by **stub functions** that simulate a summary  
  - Designed to be swapped for a real VLM such as **Qwen3-VL-4B-Instruct** or **Phi-4-Vision-Instruct**

- **RAG grounding (stub)**
  - Simple rule-based context retrieval implemented in `rag.py`
  - Returns topic-specific educational paragraphs (AMH, age, PCOS, ovarian reserve, etc.)
  - Prepared to be replaced by **GraphRAG** or **FAISS + LlamaIndex** with 100–200 fertility PDFs

- **Safety by design**
  - Every answer includes a medical disclaimer
  - Explanations are educational, non-prescriptive
  - No drug names, dosages, or treatment plans suggested

- **Tanit.ai branding**
  - Header with Tanit.ai logo
  - Color palette inspired by Tanit’s visual identity (purple + teal)
  - Clean, clinic-style layout focused on usability

---

## 2. Tech Stack

- **Language:** Python 3
- **UI:** [Gradio](https://gradio.app/)
- **STT:** [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (local speech-to-text)
- **Potential VLMs (not fully wired yet):**
  - Qwen3-VL-4B-Instruct
  - Phi-4-Vision-Instruct
  - LLaVA / Florence-2 (future options)
- **RAG (current):** simple keyword-based stub in `rag.py`
- **RAG (planned):** Microsoft GraphRAG or LlamaIndex + FAISS

---

## 3. Repository Structure

```text
tanit-multimodal-fertility-assistant/
├── app.py                   # Main Gradio app (single-page chatbot)
├── rag.py                   # RAG stub (topic-based fertility context)
├── vlm.py                   # Stubs for image/PDF analysis (VLM-ready)
├── voice/
│   ├── __init__.py
│   └── stt.py               # Speech-to-text wrapper (faster-whisper)
├── assets/
│   ├── logo.png             # Tanit.ai logo used in the header
│   └── style.css            # Custom CSS for branding and layout
├── requirements.txt         # Python dependencies
├── kaggle_notebook.ipynb    # Kaggle demo: install + launch + backend tests
└── report.pdf               # 3–6 page written report (architecture, models, safety)
