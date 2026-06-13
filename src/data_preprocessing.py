"""
data_preprocessing.py
----------------------
Membaca, membersihkan, dan memisahkan (split) dataset parallel
Indonesia-Sunda yang telah diunduh dari OPUS.
"""

import re
import pandas as pd
from datasets import Dataset, DatasetDict


# --- Path default ---
RAW_ID_FILE  = "dataset_opus/wikimedia.id-su.id"
RAW_SU_FILE  = "dataset_opus/wikimedia.id-su.su"
CLEAN_CSV    = "dataset_translator_idsu_perfect.csv"


# ---------------------------------------------------------------------------
# Cleaning
# ---------------------------------------------------------------------------

def clean_wikipedia_noise(text: str) -> str:
    """
    Membersihkan noise khas dump Wikipedia dari sebuah string teks.

    Langkah-langkah:
    1. Hapus markup wikilink sederhana  [[Kata]] → Kata
    2. Hapus markup wikilink dengan alias [[Link|Alias]] → Alias
    3. Hapus referensi bernomor seperti [1], [2], dst.
    4. Rapi-kan spasi ganda yang tersisa.
    """
    if not isinstance(text, str):
        return ""

    # [[Kata]] → Kata
    text = re.sub(r"\[\[([^\]|]+)\]\]", r"\1", text)
    # [[Link|Alias]] → Alias
    text = re.sub(r"\[\[[^\]|]+\|([^\]]+)\]\]", r"\1", text)
    # [1] [2] dst.
    text = re.sub(r"\[\d+\]", "", text)
    # spasi ganda
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ---------------------------------------------------------------------------
# Build & clean DataFrame
# ---------------------------------------------------------------------------

def build_dataframe(
    id_file: str = RAW_ID_FILE,
    su_file: str = RAW_SU_FILE,
) -> pd.DataFrame:
    """
    Membaca file teks baris-demi-baris dan menggabungkannya ke dalam DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame dengan kolom 'ind_Latn' dan 'sun_Latn'.
    """
    with open(id_file, "r", encoding="utf-8") as f:
        ind_lines = [line.strip() for line in f]

    with open(su_file, "r", encoding="utf-8") as f:
        sun_lines = [line.strip() for line in f]

    df = pd.DataFrame({"ind_Latn": ind_lines, "sun_Latn": sun_lines})
    print(f"Total baris mentah: {len(df)}")
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Terapkan pembersihan noise Wikipedia ke kedua kolom,
    lalu buang baris yang mengandung karakter sisa '↑' di ind_Latn (sesuai notebook).
    """
    df = df.copy()
    df["ind_Latn"] = df["ind_Latn"].apply(clean_wikipedia_noise)
    df["sun_Latn"] = df["sun_Latn"].apply(clean_wikipedia_noise)

    # Buang baris yang mengandung karakter daftar pustaka '↑' di ind_Latn (sesuai dengan notebook)
    df = df[~df["ind_Latn"].str.contains("↑", na=False)]

    # Buang baris kosong / null agar menghasilkan tepat 5272 baris sesuai di paper UAS
    df = df.dropna(subset=["ind_Latn", "sun_Latn"])
    df = df[(df["ind_Latn"].str.strip() != "") & (df["sun_Latn"].str.strip() != "")]
    df = df.reset_index(drop=True)

    print(f"Jumlah baris setelah pembersihan: {len(df)}")
    return df


def save_clean_csv(df: pd.DataFrame, path: str = CLEAN_CSV) -> None:
    """Simpan DataFrame bersih ke file CSV dengan encoding utf-8-sig agar karakter aksen terbaca rapi di Excel."""
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print(f"Dataset bersih disimpan di: {path}")


# ---------------------------------------------------------------------------
# Split
# ---------------------------------------------------------------------------

def split_dataset(
    csv_path: str = CLEAN_CSV,
    test_size: float = 0.1,
    val_fraction: float = 0.5,
    seed: int = 42,
) -> DatasetDict:
    """
    Muat CSV bersih dan bagi menjadi split Train / Validation / Test.

    Pembagian default:
    - Train      : 90 %
    - Validation :  5 %
    - Test       :  5 %

    Returns
    -------
    DatasetDict
        Kamus berisi split 'train', 'validation', dan 'test'.
    """
    from datasets import load_dataset

    raw = load_dataset("csv", data_files=csv_path)

    # Buang baris yang NaN
    raw = raw.filter(
        lambda x: isinstance(x["ind_Latn"], str) and isinstance(x["sun_Latn"], str)
    )

    # Bagi menjadi train (90%) dan sisa (10%)
    split = raw["train"].train_test_split(test_size=test_size, seed=seed)

    # Bagi sisa menjadi validation dan test
    val_test = split["test"].train_test_split(test_size=val_fraction, seed=seed)

    final: DatasetDict = DatasetDict(
        {
            "train": split["train"],
            "validation": val_test["train"],
            "test": val_test["test"],
        }
    )

    print("=== Hasil Pembagian Dataset ===")
    print(f"  Train      : {len(final['train'])} baris")
    print(f"  Validation : {len(final['validation'])} baris")
    print(f"  Test       : {len(final['test'])} baris")

    return final


# ---------------------------------------------------------------------------
# One-shot pipeline helper
# ---------------------------------------------------------------------------

def prepare_dataset(
    id_file: str = RAW_ID_FILE,
    su_file: str = RAW_SU_FILE,
    clean_csv: str = CLEAN_CSV,
) -> DatasetDict:
    """
    Jalankan seluruh pipeline preprocessing dalam satu fungsi:
    build → clean → save CSV → split.
    """
    df = build_dataframe(id_file, su_file)
    df = clean_dataframe(df)
    save_clean_csv(df, clean_csv)
    return split_dataset(clean_csv)


if __name__ == "__main__":
    prepare_dataset()
