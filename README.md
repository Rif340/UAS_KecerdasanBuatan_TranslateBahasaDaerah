<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=1C_2g1apCP8nK6sUstwAs04eQEbEg3s9s" width="100%">
</p>

<h1 align="center">🌿 SISTEM PENERJEMAH BAHASA DAERAH</h1>

<p align="center">
Aplikasi sederhana ini dibuat untuk memenuhi Tugas Akhir mata kuliah Kecerdasan Buatan dengan fokus pada cabang pemrosesan bahasa alami atau <i>Natural Language Processing</i> (NLP). Sistem ini berfokus pada penerjemahan bahasa daerah.
</p>

<p align="center">
  <a href="https://uas-kecerdasanbuatan-translatebahasadaerah.streamlit.app/">
    <img src="https://img.shields.io/badge/LIVE%20DEMO-VISIT%20WEBSITE-2ea44f?style=for-the-badge&logo=googlechrome&logoColor=white">
  </a>
</p>

---

# 👥 MEET THE TEAM

**Project Akhir UAS Matakuliah Kecerdasan Buatan - Teknik Informatika**

| Nama | NPM |
|---|---|
| Aldi Wijaya | 2410631170004 |
| Muhammad Arif Wicaksono | 2410631170034 |

---

# 🚀 STATUS & FITUR PROYEK

> [!IMPORTANT]
> **Status Pengembangan:** Saat ini proyek ini **masih dalam tahap pengembangan aktif**. Fitur utama yang baru selesai dikembangkan adalah **Penerjemahan Bahasa Sunda ke Indonesia (dan sebaliknya)**. Fitur lainnya serta bahasa daerah lain (Jawa, Bugis) saat ini belum sepenuhnya dibuat/diimplementasikan dan masih berupa rancangan awal (mockup).

## 1. Language Translation (Penerjemahan Bahasa Daerah)
* **Rule-Based (Kamus & Aturan Lokal)**: Menerjemahkan kalimat/kata dari bahasa Sunda ke Indonesia (dan sebaliknya) secara terstruktur berdasarkan register bahasa (biasa/kasar).
* **Machine Learning**: Menggunakan model **Meta NLLB-200 (No Language Left Behind)** (masih dalam pengembangan/uji coba).

## 2. Fitur Lain (Rencana Pengembangan)
* **Part of Speech (POS) Tagging**: Analisis kelas kata untuk bahasa daerah (belum diimplementasikan).
* **Audio/Video Transcription & Subtitles**: Transkripsi otomatis suara/video bahasa daerah (belum diimplementasikan).

---

# 🛠️ PANDUAN INSTALASI DAN PENGGUNAAN LOKAL

### Prasyarat
Pastikan Anda sudah menginstal **Python 3.8 - 3.11** di komputer Anda.

## 1️⃣ Clone Repository
```bash
git clone https://github.com/Rif340/UAS_KecerdasanBuatan_TranslateBahasaDaerah.git
cd UAS_KecerdasanBuatan_TranslateBahasaDaerah
```

## 2️⃣ Install Dependensi
Instal pustaka-pustaka Python yang dibutuhkan:
```bash
pip install -r requirements.txt
```

## 3️⃣ Jalankan Aplikasi
Mulai server lokal Streamlit Anda dengan perintah:
```bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser Anda pada alamat `http://localhost:8501`.

---

# 📂 STRUKTUR DIREKTORI PROYEK

```text
UAS_KecerdasanBuatan_TranslateBahasaDaerah/
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

# ⚙️ CARA MEMPERBARUI DATASET (KAMUS KOSAKATA)

Untuk memperbarui kosakata atau aturan penerjemahan:
1. Buka file `Dataset/korpus nusantara.xlsx`.
2. Tambahkan kosakata baru di sheet masing-masing bahasa (`sunda`, `jawa`, atau `bugis wajo`) dengan format:
   * **Kolom A**: Kata/Kalimat dalam Bahasa Indonesia (contoh: `kamu (kasar)`).
   * **Kolom B**: Terjemahan dalam Bahasa Daerah terkait (contoh: `sia`).
3. Setelah memperbarui file Excel tersebut, jalankan aplikasi lalu tekan tombol **"Reload Dataset"** (dengan ikon refresh ↻) pada sidebar aplikasi Streamlit untuk memuat ulang dataset terbaru secara langsung tanpa perlu mematikan aplikasi.
