# UAS Kecerdasan Buatan: Translate Bahasa Daerah (Integrated Linguistic Tools)

[![Streamlit App](https://static.streamlit.io/badge_svg.svg)](https://uas-kecerdasanbuatan-translatebahasadaerah.streamlit.app)

Project ini merupakan tugas akhir mata kuliah **Kecerdasan Buatan**. Aplikasi ini dirancang sebagai platform terpadu untuk pengolahan bahasa daerah (*Integrated Linguistic Tools*), yang mencakup penerjemahan multi-bahasa, analisis kelas kata (*POS Tagging*), serta transkripsi audio/video.

## 👤 Identitas Pengembang
* **Nama:** Muhammad Arif Wicaksono
* **NPM:** 2410631170034
* **Program Studi:** Teknik Informatika
* **Tautan Web Aplikasi:** [https://uas-kecerdasanbuatan-translatebahasadaerah.streamlit.app](https://uas-kecerdasanbuatan-translatebahasadaerah.streamlit.app)

---

## 🚀 Status & Fitur Proyek
> [!IMPORTANT]
> **Status Pengembangan:** Saat ini proyek ini **masih dalam tahap pengembangan aktif**. Fitur utama yang baru selesai dikembangkan adalah **Penerjemahan Bahasa Sunda ke Indonesia (dan sebaliknya)**. Fitur lainnya serta bahasa daerah lain (Jawa, Bugis) saat ini belum sepenuhnya dibuat/diimplementasikan dan masih berupa rancangan awal (mockup).

### Fitur yang Dikembangkan:
1. **Language Translation (Penerjemahan Bahasa Daerah)**:
   * **Rule-Based (Kamus & Aturan Lokal)**: Menerjemahkan kalimat/kata dari bahasa Sunda ke Indonesia (dan sebaliknya) secara terstruktur berdasarkan register bahasa (biasa/kasar).
   * **Machine Learning**: Menggunakan model **Meta NLLB-200 (No Language Left Behind)** (masih dalam pengembangan/uji coba).
2. **Fitur Lain (Rencana Pengembangan)**:
   * **Part of Speech (POS) Tagging**: Analisis kelas kata untuk bahasa daerah (belum diimplementasikan).
   * **Audio/Video Transcription & Subtitles**: Transkripsi otomatis suara/video bahasa daerah (belum diimplementasikan).

---

## 🛠️ Panduan Instalasi dan Penggunaan Lokal

### Prasyarat
Pastikan Anda sudah menginstal **Python 3.8 - 3.11** di komputer Anda.

### Langkah-langkah
1. **Clone Repository**:
   ```bash
   git clone https://github.com/arifk/UAS_kecerdasanBuatan_TranslateBahasaDaerah.git
   cd UAS_kecerdasanBuatan_TranslateBahasaDaerah
   ```

2. **Install Dependensi**:
   Instal pustaka-pustaka Python yang dibutuhkan:
   ```bash
   pip install -r requirements.txt
   ```

3. **Jalankan Aplikasi**:
   Mulai server lokal Streamlit Anda dengan perintah:
   ```bash
   streamlit run app.py
   ```
   Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

---

## 📂 Struktur Direktori Proyek
```text
UAS_kecerdasanBuatan_TranslateBahasaDaerah/
│
├── Dataset/
│   └── korpus nusantara.xlsx     # File Excel berisi korpus kosakata bahasa daerah
│
├── app.py                         # Kode utama antarmuka (Streamlit UI)
├── translator.py                  # Logika penerjemah (Rule-Based & ML)
├── requirements.txt               # Daftar dependensi pustaka Python
└── README.md                      # Dokumentasi proyek (file ini)
```

---

## ⚙️ Cara Memperbarui Dataset (Kamus Kosakata)
Untuk memperbarui kosakata atau aturan penerjemahan:
1. Buka file `Dataset/korpus nusantara.xlsx`.
2. Tambahkan kosakata baru di sheet masing-masing bahasa (`sunda`, `jawa`, atau `bugis wajo`) dengan format:
   * **Kolom A**: Kata/Kalimat dalam Bahasa Indonesia.
   * **Kolom B**: Terjemahan dalam Bahasa Daerah terkait.
3. Setelah memperbarui file Excel tersebut, jalankan aplikasi lalu tekan tombol **"Reload Dataset"** (dengan ikon refresh ↻) pada sidebar aplikasi Streamlit untuk memuat ulang dataset terbaru secara langsung tanpa perlu mematikan aplikasi.
