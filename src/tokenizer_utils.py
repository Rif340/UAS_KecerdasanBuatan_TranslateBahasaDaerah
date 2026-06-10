"""
tokenizer_utils.py
-------------------
Memuat tokenizer NLLB-200 dan menyediakan fungsi tokenisasi
untuk kedua arah terjemahan (Indonesia → Sunda dan Sunda → Indonesia).
"""

from transformers import AutoTokenizer
from datasets import DatasetDict, concatenate_datasets


MODEL_CHECKPOINT = "facebook/nllb-200-distilled-600M"
MAX_LENGTH       = 128

# Kode bahasa resmi NLLB-200
LANG_CODE = {
    "Indonesia": "ind_Latn",
    "Sunda":     "sun_Latn",
}


def load_tokenizer(checkpoint: str = MODEL_CHECKPOINT) -> AutoTokenizer:
    """Muat tokenizer NLLB-200 dari Hugging Face Hub."""
    print(f"Memuat tokenizer dari: {checkpoint}")
    tokenizer = AutoTokenizer.from_pretrained(checkpoint)
    print("Tokenizer berhasil dimuat!")
    return tokenizer


# ---------------------------------------------------------------------------
# Fungsi preprocessing per arah
# ---------------------------------------------------------------------------

def make_preprocess_fn(
    tokenizer: AutoTokenizer,
    src_lang: str,
    tgt_lang: str,
    src_col: str,
    tgt_col: str,
    max_length: int = MAX_LENGTH,
):
    """
    Buat fungsi preprocessing yang bisa dipanggil oleh Dataset.map().

    Parameters
    ----------
    tokenizer  : Tokenizer NLLB-200 yang sudah dimuat.
    src_lang   : Kode bahasa sumber (mis. 'ind_Latn').
    tgt_lang   : Kode bahasa tujuan (mis. 'sun_Latn').
    src_col    : Nama kolom sumber di dataset.
    tgt_col    : Nama kolom tujuan di dataset.
    max_length : Panjang maksimum token.
    """

    def preprocess(examples):
        tokenizer.src_lang = src_lang
        tokenizer.tgt_lang = tgt_lang

        inputs  = [str(t) for t in examples[src_col]]
        targets = [str(t) for t in examples[tgt_col]]

        return tokenizer(
            inputs,
            text_target=targets,
            max_length=max_length,
            truncation=True,
        )

    return preprocess


def tokenize_splits(
    final_splits: DatasetDict,
    tokenizer: AutoTokenizer,
    max_length: int = MAX_LENGTH,
) -> tuple:
    """
    Tokenisasi dataset untuk kedua arah (ID→SU dan SU→ID),
    kemudian gabungkan dan acak menjadi satu dataset per split.

    Returns
    -------
    tuple
        (train_dataset_dua_arah, val_dataset_dua_arah)
    """
    fn_idsu = make_preprocess_fn(tokenizer, "ind_Latn", "sun_Latn", "ind_Latn", "sun_Latn", max_length)
    fn_suid = make_preprocess_fn(tokenizer, "sun_Latn", "ind_Latn", "sun_Latn", "ind_Latn", max_length)

    print("Tokenisasi arah Indonesia → Sunda ...")
    tok_train_idsu = final_splits["train"].map(fn_idsu, batched=True)
    tok_val_idsu   = final_splits["validation"].map(fn_idsu, batched=True)

    print("Tokenisasi arah Sunda → Indonesia ...")
    tok_train_suid = final_splits["train"].map(fn_suid, batched=True)
    tok_val_suid   = final_splits["validation"].map(fn_suid, batched=True)

    print("Menggabungkan dan mengacak dataset dua arah ...")
    train_dua_arah = concatenate_datasets([tok_train_idsu, tok_train_suid]).shuffle(seed=42)
    val_dua_arah   = concatenate_datasets([tok_val_idsu,   tok_val_suid  ]).shuffle(seed=42)

    print("=== Ukuran Dataset Dua Arah ===")
    print(f"  Train : {len(train_dua_arah)} baris")
    print(f"  Val   : {len(val_dua_arah)} baris")
    print("Tokenisasi selesai!")

    return train_dua_arah, val_dua_arah


def tokenize_test(
    final_splits: DatasetDict,
    tokenizer: AutoTokenizer,
    max_length: int = MAX_LENGTH,
):
    """
    Tokenisasi data test untuk kedua arah, lalu gabungkan.

    Returns
    -------
    Dataset gabungan test dua arah.
    """
    fn_idsu = make_preprocess_fn(tokenizer, "ind_Latn", "sun_Latn", "ind_Latn", "sun_Latn", max_length)
    fn_suid = make_preprocess_fn(tokenizer, "sun_Latn", "ind_Latn", "sun_Latn", "ind_Latn", max_length)

    tok_test_idsu = final_splits["test"].map(fn_idsu, batched=True)
    tok_test_suid = final_splits["test"].map(fn_suid, batched=True)

    test_dua_arah = concatenate_datasets([tok_test_idsu, tok_test_suid]).shuffle(seed=42)
    print(f"Jumlah data Test gabungan dua arah: {len(test_dua_arah)} baris")
    return test_dua_arah
