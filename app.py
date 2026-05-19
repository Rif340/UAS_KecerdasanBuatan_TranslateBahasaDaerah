import streamlit as st
import os
import time
from translator import RuleBasedTranslator, MLTranslator

# Set konfigurasi halaman
st.set_page_config(
    page_title="Integrated Linguistic Tools",
    page_icon="🌐",
    layout="centered"
)

# Custom CSS untuk estetika premium
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .main-header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            font-weight: 700;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .sub-header {
            font-size: 24px;
            font-weight: 600;
            color: #2a5298;
            margin-bottom: 15px;
        }
        
        .stButton>button {
            background-color: #007bff;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            border: none;
            padding: 10px 25px;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .stButton>button:hover {
            background-color: #0056b3;
            box-shadow: 0 4px 12px rgba(0,123,255,0.3);
            transform: translateY(-2px);
        }
        
        .tab-content {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #dee2e6;
            margin-top: 15px;
        }
        
        /* Style for language swap button */
        .st-key-swap_btn button {
            background-color: white !important;
            color: #007bff !important;
            border: 1px solid #ced4da !important;
            border-radius: 6px !important;
            font-weight: 600 !important;
            font-size: 20px !important;
            width: 46px !important;
            height: 40px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 28px auto 0 auto !important;
            transform: translateX(8px) !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
            transition: all 0.2s ease !important;
        }
        
        .st-key-swap_btn button:hover {
            background-color: #f8f9fa !important;
            border-color: #b5bbc1 !important;
            transform: translateX(8px) !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Header Utama
st.markdown("<div class='main-header'><h1>Integrated Linguistic Tools</h1></div>", unsafe_allow_html=True)

# Inisialisasi Translator dengan session_state agar bisa di-reload
excel_path = os.path.join("Dataset", "korpus nusantara.xlsx")

# Load translator ke session_state (hanya sekali, kecuali di-reload)
if "rule_translator" not in st.session_state:
    st.session_state["rule_translator"] = RuleBasedTranslator(excel_path)
if "ml_translator" not in st.session_state:
    st.session_state["ml_translator"] = MLTranslator()

rule_translator = st.session_state["rule_translator"]
ml_translator = st.session_state["ml_translator"]

# Sidebar: tombol reload dataset
with st.sidebar:
    st.markdown("### ⚙️ Pengaturan")
    if st.button("Reload Dataset", icon=":material/refresh:", help="Klik ini setelah Anda mengupdate file Excel agar perubahan terbaca", key="reload_dataset_btn_sidebar"):
        if "rule_translator" in st.session_state:
            del st.session_state["rule_translator"]
        st.success("Dataset berhasil di-reload!")
        st.rerun()
    abs_excel_path = os.path.abspath(excel_path)
    st.caption("📁 Path Dataset yang Dibaca:")
    st.code(abs_excel_path, language="text")
    st.info("💡 Pastikan Anda mengedit file Excel di path di atas agar kosakata baru terdeteksi oleh aplikasi ini.")

# Membuat Tabs sesuai gambar
tabs = st.tabs([
    "Translation", 
    "Part of Speech Tagging", 
    "Audio Transcription", 
    "Video Transcription", 
    "Video Subtitle Generation"
])

# ==================== TAB 1: TRANSLATION ====================
with tabs[0]:
    st.markdown("<div class='sub-header'>Language Translation</div>", unsafe_allow_html=True)
    
    # Memilih metode AI
    method = st.radio(
        "Pilih Metode AI Penerjemah:",
        ("Rule-Based (Kamus & Aturan Lokal)", "Machine Learning (Meta NLLB-200 - Butuh GPU/Internet)"),
        horizontal=True
    )
    
    # Inisialisasi session state untuk pilihan bahasa jika belum ada
    if "source_lang" not in st.session_state:
        st.session_state["source_lang"] = "Indonesia"
    if "target_lang" not in st.session_state:
        st.session_state["target_lang"] = "Sunda"

    # Callback untuk swap bahasa (dijalankan sebelum rerun)
    def swap_languages():
        src = st.session_state["source_lang"]
        tgt = st.session_state["target_lang"]
        st.session_state["source_lang"] = tgt
        st.session_state["target_lang"] = src

    # Pilihan Bahasa
    col1, col_swap, col2 = st.columns([4, 1, 4])
    languages = ["Indonesia", "Sunda", "Jawa", "Bugis"]
    
    with col1:
        source_lang = st.selectbox("Source Language", languages, key="source_lang")
    
    with col_swap:
        st.button("⇄", key="swap_btn", on_click=swap_languages)
            
    with col2:
        target_lang = st.selectbox("Target Language", languages, key="target_lang")

    # Pilih tingkat kesopanan untuk Rule-Based terjemahan Indonesia -> Daerah
    register = None
    if method == "Rule-Based (Kamus & Aturan Lokal)" and source_lang == "Indonesia" and target_lang in ["Sunda", "Jawa"]:
        reg_selection = st.selectbox(
            "Pilih Tingkat Kesopanan Bahasa daerah:",
            ("Biasa / Loma / Ngoko", "Kasar / Akrab")
        )
        register = "biasa" if "Biasa" in reg_selection else "kasar"

    # Input Text
    text_to_translate = st.text_area("Enter Text to Translate", placeholder="Ketik kalimat di sini...", height=150)
    
    # Tombol Terjemahkan
    if st.button("Translate", key="translate_btn"):
        if not text_to_translate.strip():
            st.warning("Silakan masukkan teks terlebih dahulu.")
        else:
            with st.spinner("Sedang menerjemahkan..."):
                if method == "Rule-Based (Kamus & Aturan Lokal)":
                    result = rule_translator.translate(text_to_translate, source_lang, target_lang, register=register)
                else:
                    # Load model machine learning lazily
                    ml_translator.load_model()
                    result = ml_translator.translate(text_to_translate, source_lang, target_lang)
                
                st.markdown("### Translated Text:")
                st.info(result)

# ==================== TAB 2: PART OF SPEECH TAGGING ====================
with tabs[1]:
    st.markdown("<div class='sub-header'>Part of Speech Tagging (POS Tagging)</div>", unsafe_allow_html=True)
    st.write("Analisis kelas kata (Kata Benda, Kerja, Sifat, dll.) untuk kalimat bahasa daerah.")
    
    pos_text = st.text_input("Masukkan Kalimat untuk di-Tag", "Pamarintah geus masihan bantuan sosial")
    
    if st.button("Analyze POS Tags", key="pos_btn"):
        words = pos_text.translate(str.maketrans("", "", "")).split()
        
        # Kamus POS Tagging sederhana (mock up cerdas berdasarkan kosakata umum)
        pos_rules = {
            # Sunda
            "pamarintah": "Noun (Kata Benda)", "pemerintah": "Noun (Kata Benda)",
            "geus": "Adverb (Kata Keterangan)", "sudah": "Adverb (Kata Keterangan)",
            "masihan": "Verb (Kata Kerja)", "memberikan": "Verb (Kata Kerja)",
            "bantuan": "Noun (Kata Benda)",
            "sosial": "Adjective (Kata Sifat)",
            # Jawa
            "bapak": "Noun (Kata Benda)", "ibu": "Noun (Kata Benda)",
            "mangan": "Verb (Kata Kerja)", "dahar": "Verb (Kata Kerja)",
            "sego": "Noun (Kata Benda)", "sekul": "Noun (Kata Benda)"
        }
        
        tagged_output = []
        for word in words:
            word_clean = word.lower().strip()
            tag = pos_rules.get(word_clean, "Noun/Other (Belum Terindeks)")
            tagged_output.append({"Word": word, "POS Tag": tag})
            
        st.table(tagged_output)

# ==================== TAB 3: AUDIO TRANSCRIPTION ====================
with tabs[2]:
    st.markdown("<div class='sub-header'>Audio Transcription</div>", unsafe_allow_html=True)
    st.write("Unggah rekaman suara bahasa daerah untuk diubah menjadi teks secara otomatis.")
    
    audio_file = st.file_uploader("Unggah File Audio (.wav, .mp3)", type=["wav", "mp3"])
    
    if audio_file is not None:
        st.audio(audio_file)
        if st.button("Transcribe Audio", key="audio_btn"):
            with st.spinner("Sedang memproses audio..."):
                time.sleep(2)  # simulasi proses
                st.success("Transkripsi Selesai!")
                # Mock result atau tampilkan teks tiruan
                st.info("Hasil Transkripsi: \"Abdi bade angkat ka sakola enjing-enjing\" (Sunda)")

# ==================== TAB 4: VIDEO TRANSCRIPTION ====================
with tabs[3]:
    st.markdown("<div class='sub-header'>Video Transcription</div>", unsafe_allow_html=True)
    st.write("Unggah file video untuk mengekstrak transkrip percakapan bahasa daerah.")
    
    video_file = st.file_uploader("Unggah File Video (.mp4)", type=["mp4"])
    
    if video_file is not None:
        st.video(video_file)
        if st.button("Transcribe Video", key="video_btn"):
            with st.spinner("Mengekstrak audio dan mentranskripsi..."):
                time.sleep(3)
                st.success("Transkripsi Video Selesai!")
                st.info("Hasil Transkripsi: \"Matur nuwun sanget atas bantuanipun bapak ibu sekalian\" (Jawa)")

# ==================== TAB 5: VIDEO SUBTITLE GENERATION ====================
with tabs[4]:
    st.markdown("<div class='sub-header'>Video Subtitle Generation</div>", unsafe_allow_html=True)
    st.write("Membuat file subtitle (.srt) otomatis untuk video bahasa daerah beserta terjemahannya.")
    
    sub_video_file = st.file_uploader("Unggah Video untuk Pembuatan Subtitle", type=["mp4"], key="sub_video")
    
    if sub_video_file is not None:
        if st.button("Generate Subtitles", key="sub_btn"):
            with st.spinner("Membuat file subtitle SRT..."):
                time.sleep(4)
                st.success("Subtitle Berhasil Dibuat!")
                
                # Menampilkan contoh isi file SRT
                srt_content = """1
00:00:01,000 --> 00:00:04,000
[Sunda] Wilujeng sumping di bumi abdi.
(Selamat datang di rumah saya.)

2
00:00:04,500 --> 00:00:08,000
[Sunda] Mangga kalebet, tos disayagikeun tuangeun.
(Silakan masuk, sudah disediakan makanan.)"""
                
                st.code(srt_content, language="srt")
                st.download_button(
                    label="Unduh File Subtitle (.srt)",
                    data=srt_content,
                    file_name="subtitles.srt",
                    mime="text/plain"
                )
