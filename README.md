# 🌐 NLLB-200 Fine-tuned Translator: Indonesia ↔ Sunda

Fine-tuning model terjemahan neural **NLLB-200** milik Meta AI untuk pasangan bahasa **Indonesia ↔ Sunda** menggunakan dataset paralel dari OPUS Wikimedia. Model dilatih secara **bidirectional** (dua arah sekaligus: ID→SU dan SU→ID).

---

## 📋 Daftar Isi

- [Gambaran Proyek](#gambaran-proyek)
- [Struktur Proyek](#struktur-proyek)
- [Prasyarat & Instalasi](#prasyarat--instalasi)
- [Cara Menjalankan Training](#cara-menjalankan-training)
- [Cara Menjalankan UI Translator](#cara-menjalankan-ui-translator)
- [Penjelasan Modul](#penjelasan-modul)
- [Konfigurasi Training](#konfigurasi-training)
- [Catatan Teknis](#catatan-teknis)

---

## 🧠 Gambaran Proyek

| Komponen | Detail |
|---|---|
| **Base Model** | `facebook/nllb-200-distilled-600M` |
| **Dataset** | OPUS Wikimedia `id-su` (v20230407) |
| **Arah Terjemahan** | Indonesia → Sunda **dan** Sunda → Indonesia |
| **Metrik Evaluasi** | SacreBLEU |
| **UI** | Gradio (berjalan di browser lokal) |

---

## 📁 Struktur Proyek

```
nllb-id-su-translator/
│
├── src/                            # Modul-modul inti
│   ├── __init__.py
│   ├── data_download.py            # Unduh & ekstrak dataset OPUS
│   ├── data_preprocessing.py       # Bersihkan & split dataset
│   ├── tokenizer_utils.py          # Muat tokenizer & tokenisasi
│   ├── metrics.py                  # Fungsi evaluasi BLEU
│   └── trainer.py                  # Fine-tuning & evaluasi model
│
├── train.py                        # Script utama training (jalankan ini)
├── app.py                          # UI Gradio untuk translator
├── requirements.txt                # Daftar dependensi Python
├── .gitignore
└── README.md
```

---

## ⚙️ Prasyarat & Instalasi

### 1. Prasyarat Sistem

- **Python** ≥ 3.10
- **GPU** dengan CUDA (sangat direkomendasikan untuk training). CPU bisa digunakan tapi sangat lambat.
- Ruang disk minimal **5 GB** (untuk model, dataset, dan checkpoint)

### 2. Buat Virtual Environment (Direkomendasikan)

```bash
# Buat virtual environment
python -m venv .venv

# Aktifkan (Windows)
.venv\Scripts\activate

# Aktifkan (Linux / macOS)
source .venv/bin/activate
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

> **Catatan untuk pengguna GPU:** Pastikan PyTorch versi CUDA sudah terinstal dengan benar.  
> Cek di: https://pytorch.org/get-started/locally/

---

## 🚀 Cara Menjalankan Training

Jalankan script utama dari direktori proyek:

```bash
python train.py
```

Script ini akan menjalankan **seluruh pipeline** secara otomatis:

| Langkah | Keterangan |
|:---:|---|
| **1** | Unduh dataset paralel ID-SU dari OPUS Wikimedia |
| **2** | Ekstrak & bersihkan dataset (hapus noise Wikipedia) |
| **3** | Split dataset: Train (90%) / Validation (5%) / Test (5%) |
| **4** | Muat tokenizer NLLB-200 & tokenisasi dataset dua arah |
| **5** | Muat model & jalankan fine-tuning (3 epoch) |
| **6** | Evaluasi akhir pada test set (skor BLEU) |
| **7** | Simpan model ke `./translator_dua_arah_final/` |

> ⏱️ **Estimasi Waktu:**  
> - Dengan GPU (A100): ~2–4 jam  
> - Dengan GPU (V100/T4): ~4–8 jam  
> - Dengan CPU saja: Tidak praktis untuk training penuh

---

## 🖥️ Cara Menjalankan UI Translator

Setelah model selesai dilatih (folder `translator_dua_arah_final/` sudah ada):

```bash
python app.py
```

Browser akan terbuka otomatis di `http://localhost:7860`. Fitur UI:

- 🔄 Pilih arah terjemahan (Indonesia → Sunda atau Sunda → Indonesia)
- ⇄ Tombol tukar bahasa
- 📝 Input teks dan tampilan hasil terjemahan
- 💡 Contoh kalimat tersedia langsung di UI

---

## 📦 Penjelasan Modul

### `src/data_download.py`
Mengunduh file zip dataset paralel dari server OPUS dan mengekstraknya ke folder `dataset_opus/`. Melewati unduhan jika file sudah ada (idempoten).

**Fungsi utama:**
- `download_and_extract()` — unduh dan ekstrak sekaligus

---

### `src/data_preprocessing.py`
Membaca pasangan kalimat dari file teks mentah, membersihkan noise khas dump Wikipedia (markup wikilink, referensi angka, spasi ganda, karakter `↑`), dan membagi dataset.

**Fungsi utama:**
- `clean_wikipedia_noise(text)` — bersihkan satu string teks
- `prepare_dataset()` — pipeline lengkap: baca → bersihkan → simpan CSV → split

---

### `src/tokenizer_utils.py`
Memuat tokenizer NLLB-200 dan menyediakan fungsi untuk tokenisasi dataset dalam dua arah. Dataset dua arah digabungkan dan diacak agar model belajar secara seimbang.

**Fungsi utama:**
- `load_tokenizer(checkpoint)` — muat tokenizer
- `tokenize_splits(final_splits, tokenizer)` — tokenisasi train & val dua arah
- `tokenize_test(final_splits, tokenizer)` — tokenisasi test dua arah

---

### `src/metrics.py`
Menyediakan fungsi evaluasi SacreBLEU yang kompatibel dengan `Seq2SeqTrainer`.

**Fungsi utama:**
- `build_compute_metrics(tokenizer)` — buat fungsi `compute_metrics` yang siap dipakai trainer

---

### `src/trainer.py`
Mengelola seluruh siklus training: konfigurasi argumen, inisialisasi `Seq2SeqTrainer`, training, evaluasi, dan penyimpanan model.

**Fungsi utama:**
- `load_model(checkpoint)` — muat model dari HuggingFace/path lokal
- `build_trainer(...)` — buat `Seq2SeqTrainer` dengan konfigurasi lengkap
- `run_training(trainer)` — jalankan fine-tuning
- `evaluate_model(trainer, test_dataset)` — evaluasi pada test set
- `save_model(trainer, tokenizer, output_dir)` — simpan model

---

## 🔧 Konfigurasi Training

Konfigurasi training bisa diubah di file `train.py` pada variabel `TRAINING_ARGS_OVERRIDE`:

```python
TRAINING_ARGS_OVERRIDE = {
    "num_train_epochs": 5,        # Tambah epoch
    "learning_rate": 1e-5,        # Turunkan learning rate
    "fp16": False,                 # Matikan half-precision (untuk CPU/GPU lama)
    "per_device_train_batch_size": 4,  # Kurangi batch size jika VRAM terbatas
}
```

Nilai default training tersedia di `src/trainer.py` → `DEFAULT_TRAINING_ARGS`.

---

## 📝 Catatan Teknis

### Tentang fp16 (Half Precision)
```python
# Di src/trainer.py → DEFAULT_TRAINING_ARGS
"fp16": True,  # Atur ke False jika:
               # - Tidak ada GPU
               # - GPU tidak mendukung half-precision (GPU lama)
               # - Menggunakan Apple Silicon (gunakan bf16=True)
```

### Tentang Model yang Digunakan
Model `facebook/nllb-200-distilled-600M` adalah versi *distilled* (lebih kecil & cepat) dari NLLB-200. Tersedia juga versi yang lebih besar:
- `facebook/nllb-200-1.3B` — lebih akurat, lebih lambat
- `facebook/nllb-200-3.3B` — paling akurat, butuh GPU besar

Untuk menggantinya, ubah `MODEL_CHECKPOINT` di `train.py`.

### Tentang Dataset OPUS
Dataset berasal dari [OPUS Wikimedia](https://opus.nlpl.eu/) yang berisi pasangan kalimat dari Wikipedia dalam berbagai bahasa. Dataset ini bersifat publik dan bebas digunakan.

---

## 📄 Lisensi

Kode proyek ini bebas digunakan dan dimodifikasi. Model NLLB-200 menggunakan lisensi [CC-BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/).
