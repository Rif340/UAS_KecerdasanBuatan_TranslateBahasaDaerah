"""
data_download.py
----------------
Mengunduh dan mengekstrak dataset parallel Indonesia-Sunda dari OPUS (wikimedia).
"""

import os
import zipfile
import requests


OPUS_URL = "https://object.pouta.csc.fi/OPUS-wikimedia/v20230407/moses/id-su.txt.zip"
ZIP_PATH  = "id-su.txt.zip"
EXTRACT_DIR = "dataset_opus"


def download_dataset(url: str = OPUS_URL, zip_path: str = ZIP_PATH) -> None:
    """Unduh file zip dari URL dan simpan ke disk."""
    print(f"Sedang mengunduh dataset dari OPUS: {url}")
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(zip_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    print(f"Unduhan selesai! File disimpan di: {zip_path}")


def extract_dataset(zip_path: str = ZIP_PATH, extract_dir: str = EXTRACT_DIR) -> None:
    """Ekstrak file zip ke direktori tujuan."""
    print(f"Sedang mengekstrak file ke '{extract_dir}'...")
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    print(f"Ekstrak selesai! Isi folder: {os.listdir(extract_dir)}")


def download_and_extract(
    url: str = OPUS_URL,
    zip_path: str = ZIP_PATH,
    extract_dir: str = EXTRACT_DIR,
) -> None:
    """Unduh dan ekstrak dataset sekaligus (one-shot helper)."""
    if not os.path.exists(zip_path):
        download_dataset(url, zip_path)
    else:
        print(f"File zip sudah ada ({zip_path}), melewati unduhan.")

    if not os.path.exists(extract_dir) or len(os.listdir(extract_dir)) == 0:
        extract_dataset(zip_path, extract_dir)
    else:
        print(f"Folder '{extract_dir}' sudah ada dan tidak kosong, melewati ekstraksi.")


if __name__ == "__main__":
    download_and_extract()
