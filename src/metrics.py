"""
metrics.py
----------
Fungsi evaluasi untuk model terjemahan: SacreBLEU.
"""

import numpy as np
import evaluate
from transformers import AutoTokenizer


def load_metric():
    """Muat metrik SacreBLEU dari library evaluate."""
    return evaluate.load("sacrebleu")


def postprocess_text(
    preds: list[str],
    labels: list[str],
) -> tuple[list[str], list[list[str]]]:
    """
    Bersihkan whitespace pada hasil prediksi dan label.

    SacreBLEU mengharapkan label sebagai list-of-list
    (tiap kalimat bisa memiliki lebih dari satu referensi).
    """
    preds  = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]
    return preds, labels


def build_compute_metrics(tokenizer: AutoTokenizer):
    """
    Buat fungsi `compute_metrics` yang kompatibel dengan Seq2SeqTrainer.

    Parameters
    ----------
    tokenizer : Tokenizer yang digunakan untuk decode token ID.

    Returns
    -------
    Callable
        Fungsi yang menerima (preds, labels) dan mengembalikan dict BLEU.
    """
    metric = load_metric()

    def compute_metrics(eval_preds):
        preds, labels = eval_preds

        if isinstance(preds, tuple):
            preds = preds[0]

        decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

        # Ganti token padding (-100) dengan pad_token_id sebelum decoding
        labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
        decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

        decoded_preds, decoded_labels = postprocess_text(decoded_preds, decoded_labels)

        result = metric.compute(predictions=decoded_preds, references=decoded_labels)
        return {"bleu": result["score"]}

    return compute_metrics
