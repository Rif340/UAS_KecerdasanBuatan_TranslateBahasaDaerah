"""
app.py
------
UI Translator Indonesia ↔ Sunda menggunakan Gradio.
Dapat dijalankan secara lokal (tidak memerlukan Jupyter/Colab).

Cara menjalankan:
    python app.py

Pastikan model sudah dilatih terlebih dahulu dengan:
    python train.py
"""

import torch
import gradio as gr
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer


# -----------------------------------------------------------------------
# Konfigurasi
# -----------------------------------------------------------------------

MODEL_DIR = "./translator_dua_arah_final"

LANG_CODE = {
    "Indonesia": "ind_Latn",
    "Sunda":     "sun_Latn",
}

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# -----------------------------------------------------------------------
# Muat Model & Tokenizer
# -----------------------------------------------------------------------

print(f"Memuat model dari: {MODEL_DIR}")
print(f"Device yang digunakan: {DEVICE}")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model     = AutoModelForSeq2SeqLM.from_pretrained(MODEL_DIR).to(DEVICE)

print("Model siap digunakan!")


# -----------------------------------------------------------------------
# Fungsi Terjemahan
# -----------------------------------------------------------------------

def translate(text: str, src_lang: str, tgt_lang: str) -> str:
    """
    Terjemahkan teks dari bahasa sumber ke bahasa tujuan.

    Parameters
    ----------
    text     : Teks yang akan diterjemahkan.
    src_lang : Nama bahasa sumber ('Indonesia' atau 'Sunda').
    tgt_lang : Nama bahasa tujuan ('Indonesia' atau 'Sunda').

    Returns
    -------
    str
        Hasil terjemahan.
    """
    if not text.strip():
        return "⚠️ Teks tidak boleh kosong."

    if src_lang == tgt_lang:
        return "⚠️ Bahasa asal dan tujuan tidak boleh sama."

    src_code = LANG_CODE.get(src_lang)
    tgt_code = LANG_CODE.get(tgt_lang)

    if not src_code or not tgt_code:
        return "⚠️ Bahasa tidak didukung."

    tokenizer.src_lang = src_code

    inputs = tokenizer(text, return_tensors="pt").to(DEVICE)

    forced_bos_token_id = tokenizer.convert_tokens_to_ids(tgt_code)
    outputs = model.generate(
        **inputs,
        forced_bos_token_id=forced_bos_token_id,
        max_length=128,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


# -----------------------------------------------------------------------
# Gradio UI
# -----------------------------------------------------------------------

CSS = """
body { font-family: 'Inter', 'Segoe UI', sans-serif; }
.title-block {
    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
    padding: 24px;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 20px;
}
.title-block h1 { margin: 0; font-size: 24px; font-weight: 700; }
.title-block p  { margin: 6px 0 0; font-size: 14px; opacity: 0.85; }
"""

with gr.Blocks(css=CSS, title="NLLB Translator ID ↔ SU") as demo:

    gr.HTML("""
    <div class="title-block">
        <h1>🌐 NLLB-200 Fine-tuned Translator</h1>
        <p>Terjemahan Bidirectional: Bahasa Indonesia ↔ Bahasa Sunda</p>
    </div>
    """)

    with gr.Row():
        src_lang = gr.Dropdown(
            choices=["Indonesia", "Sunda"],
            value="Indonesia",
            label="Bahasa Sumber",
        )
        swap_btn = gr.Button("⇄ Tukar", variant="secondary", scale=0)
        tgt_lang = gr.Dropdown(
            choices=["Indonesia", "Sunda"],
            value="Sunda",
            label="Bahasa Tujuan",
        )

    with gr.Row():
        input_text = gr.Textbox(
            label="Teks yang akan diterjemahkan",
            placeholder="Ketik kalimat di sini...",
            lines=5,
        )
        output_text = gr.Textbox(
            label="Hasil Terjemahan",
            lines=5,
            interactive=False,
        )

    translate_btn = gr.Button("🔄 Terjemahkan", variant="primary")

    gr.Examples(
        examples=[
            ["Selamat pagi, apa kabar?", "Indonesia", "Sunda"],
            ["Wilujeng énjing, kumaha damang?", "Sunda", "Indonesia"],
            ["Saya ingin belajar bahasa Sunda.", "Indonesia", "Sunda"],
        ],
        inputs=[input_text, src_lang, tgt_lang],
    )

    # --- Event Handlers ---

    def swap_languages(src, tgt):
        return tgt, src

    swap_btn.click(
        fn=swap_languages,
        inputs=[src_lang, tgt_lang],
        outputs=[src_lang, tgt_lang],
    )

    translate_btn.click(
        fn=translate,
        inputs=[input_text, src_lang, tgt_lang],
        outputs=output_text,
    )

    # Enter key juga bisa memicu terjemahan
    input_text.submit(
        fn=translate,
        inputs=[input_text, src_lang, tgt_lang],
        outputs=output_text,
    )


if __name__ == "__main__":
    demo.launch(share=False, inbrowser=True)
