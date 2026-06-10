"""
train.py
--------
Script utama untuk menjalankan seluruh pipeline pelatihan:
  1. Unduh & ekstrak dataset OPUS
  2. Preprocessing & split dataset
  3. Muat tokenizer & tokenisasi dataset
  4. Muat model & jalankan fine-tuning
  5. Evaluasi akhir
  6. Simpan model

Cara menjalankan:
    python train.py
"""

from src.data_download import download_and_extract
from src.data_preprocessing import prepare_dataset
from src.tokenizer_utils import load_tokenizer, tokenize_splits, tokenize_test
from src.trainer import (
    load_model,
    build_trainer,
    run_training,
    evaluate_model,
    save_model,
)

# --- Konfigurasi ---
MODEL_CHECKPOINT = "facebook/nllb-200-distilled-600M"
MODEL_SAVE_DIR   = "./translator_dua_arah_final"

# Timpa konfigurasi training jika perlu (opsional)
TRAINING_ARGS_OVERRIDE = {
    # Contoh: ubah jumlah epoch
    # "num_train_epochs": 5,

    # Atur fp16=False jika tidak ada GPU yang mendukung half-precision
    # "fp16": False,
}


def main():
    # ------------------------------------------------------------------ #
    # 1. Unduh & Ekstrak Dataset                                          #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("LANGKAH 1: Unduh & Ekstrak Dataset OPUS")
    print("=" * 60)
    download_and_extract()

    # ------------------------------------------------------------------ #
    # 2. Preprocessing & Split                                            #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("LANGKAH 2: Preprocessing & Split Dataset")
    print("=" * 60)
    final_splits = prepare_dataset()

    # ------------------------------------------------------------------ #
    # 3. Tokenizer & Tokenisasi                                           #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("LANGKAH 3: Tokenisasi Dataset")
    print("=" * 60)
    tokenizer = load_tokenizer(MODEL_CHECKPOINT)
    train_dataset, val_dataset = tokenize_splits(final_splits, tokenizer)
    test_dataset = tokenize_test(final_splits, tokenizer)

    # ------------------------------------------------------------------ #
    # 4. Muat Model & Fine-Tuning                                         #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("LANGKAH 4: Fine-Tuning Model NLLB-200")
    print("=" * 60)
    model   = load_model(MODEL_CHECKPOINT)
    trainer = build_trainer(
        model,
        tokenizer,
        train_dataset,
        val_dataset,
        TRAINING_ARGS_OVERRIDE or None,
    )
    run_training(trainer)

    # ------------------------------------------------------------------ #
    # 5. Evaluasi Akhir                                                   #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("LANGKAH 5: Evaluasi Akhir pada Test Set")
    print("=" * 60)
    evaluate_model(trainer, test_dataset)

    # ------------------------------------------------------------------ #
    # 6. Simpan Model                                                     #
    # ------------------------------------------------------------------ #
    print("\n" + "=" * 60)
    print("LANGKAH 6: Menyimpan Model")
    print("=" * 60)
    save_model(trainer, tokenizer, MODEL_SAVE_DIR)

    print("\n✅ Seluruh pipeline training selesai!")
    print(f"   Model tersimpan di: {MODEL_SAVE_DIR}")
    print("   Jalankan 'python app.py' untuk membuka UI translator.")


if __name__ == "__main__":
    main()
