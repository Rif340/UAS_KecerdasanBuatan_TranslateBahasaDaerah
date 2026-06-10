"""
trainer.py
----------
Memuat model NLLB-200, mengonfigurasi Seq2SeqTrainer,
menjalankan fine-tuning, evaluasi akhir, dan menyimpan model.
"""

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    Seq2SeqTrainer,
    Seq2SeqTrainingArguments,
)
from datasets import Dataset

from src.metrics import build_compute_metrics


# ---------------------------------------------------------------------------
# Konfigurasi default training
# ---------------------------------------------------------------------------

DEFAULT_TRAINING_ARGS = dict(
    output_dir="./hasil_riset_nllb_bidirectional",
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    weight_decay=0.01,
    save_total_limit=2,
    num_train_epochs=3,
    predict_with_generate=True,
    fp16=True,          # Atur ke False jika tidak ada GPU / GPU tidak mendukung fp16
    report_to="none",
)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def load_model(checkpoint: str) -> AutoModelForSeq2SeqLM:
    """Muat model Seq2Seq dari Hugging Face Hub atau path lokal."""
    print(f"Memuat model dari: {checkpoint}")
    model = AutoModelForSeq2SeqLM.from_pretrained(checkpoint)
    print("Model berhasil dimuat!")
    return model


def build_trainer(
    model: AutoModelForSeq2SeqLM,
    tokenizer: AutoTokenizer,
    train_dataset: Dataset,
    eval_dataset: Dataset,
    training_args_override: dict | None = None,
) -> Seq2SeqTrainer:
    """
    Buat Seq2SeqTrainer dengan konfigurasi lengkap.

    Parameters
    ----------
    model              : Model NLLB yang sudah dimuat.
    tokenizer          : Tokenizer yang sesuai.
    train_dataset      : Dataset untuk pelatihan.
    eval_dataset       : Dataset untuk validasi.
    training_args_override : Dict untuk menimpa nilai-nilai dalam DEFAULT_TRAINING_ARGS.

    Returns
    -------
    Seq2SeqTrainer
    """
    args_dict = {**DEFAULT_TRAINING_ARGS}
    if training_args_override:
        args_dict.update(training_args_override)

    training_args = Seq2SeqTrainingArguments(**args_dict)
    data_collator  = DataCollatorForSeq2Seq(tokenizer, model=model)
    compute_metrics = build_compute_metrics(tokenizer)

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    return trainer


def run_training(trainer: Seq2SeqTrainer) -> None:
    """Jalankan proses fine-tuning."""
    print("Memulai Fine-Tuning Dua Arah...")
    trainer.train()
    print("Fine-Tuning selesai!")


def evaluate_model(trainer: Seq2SeqTrainer, test_dataset: Dataset) -> dict:
    """
    Evaluasi model pada data test dan tampilkan hasilnya.

    Returns
    -------
    dict
        Hasil evaluasi dari trainer.
    """
    print("Mengevaluasi model pada data test ...")
    results = trainer.evaluate(eval_dataset=test_dataset)

    print("\n=== HASIL UJIAN AKHIR (TEST SET DUA ARAH) ===")
    print(f"  Final BLEU Score : {results.get('eval_bleu', 'N/A'):.2f}")
    print(f"  Final Loss       : {results.get('eval_loss', 'N/A'):.4f}")

    return results


def save_model(
    trainer: Seq2SeqTrainer,
    tokenizer: AutoTokenizer,
    output_dir: str = "./translator_dua_arah_final",
) -> None:
    """Simpan model dan tokenizer yang sudah di-fine-tune."""
    trainer.save_model(output_dir)
    tokenizer.save_pretrained(output_dir)
    print(f"Model dua arah berhasil disimpan di: {output_dir}")
