import os
import pandas as pd
import string

# Mapping bahasa ke kode bahasa NLLB-200 Meta
NLLB_CODE_MAP = {
    "Indonesia": "ind_Latn",
    "Sunda": "sun_Latn",
    "Jawa": "jav_Latn",
    "Bugis": "bug_Latn"
}

# Mapping nama sheet di Excel korpus nusantara
EXCEL_SHEET_MAP = {
    "Sunda": "sunda",
    "Jawa": "jawa",
    "Bugis": "bugis wajo"  # menggunakan salah satu sheet Bugis
}

class RuleBasedTranslator:
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.sentence_dicts = {}  # { 'Sunda': { 'indo_text': 'sunda_text', ... } }
        self.word_dicts = {}      # { 'Sunda': { 'indo_word': 'sunda_word', ... } }
        self.load_corpus()

    def clean_text(self, text):
        if not isinstance(text, str):
            return ""
        return text.strip().lower().translate(str.maketrans("", "", string.punctuation))

    def load_corpus(self):
        if not os.path.exists(self.excel_path):
            print(f"Dataset Excel tidak ditemukan di: {self.excel_path}")
            return
        
        import re
        try:
            xls = pd.ExcelFile(self.excel_path)
            for lang, sheet_name in EXCEL_SHEET_MAP.items():
                if sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name, header=None)
                    # Ambil kolom 0 (Indonesian) dan kolom 1 (Daerah)
                    df = df.dropna(subset=[0, 1])
                    
                    self.sentence_dicts[lang] = {}
                    self.word_dicts[lang] = {}
                    
                    for _, row in df.iterrows():
                        indo_sent = str(row[0]).strip()
                        local_sent = str(row[1]).strip()
                        
                        # Simpan pemetaan kalimat (case-insensitive key)
                        self.sentence_dicts[lang][indo_sent.lower()] = local_sent
                        
                        # Cek apakah baris ini berisi kata dengan register, misal "saya (biasa)"
                        match = re.match(r'^([^(]+)\s*\(([^)]+)\)$', indo_sent)
                        if match:
                            w_indo = match.group(1).strip().lower()
                            reg = match.group(2).strip().lower()
                            w_local = local_sent.strip().lower()
                            
                            # Simpan dengan kunci register
                            self.word_dicts[lang][f"{w_indo} ({reg})"] = w_local
                            
                            # Simpan kata dasar polos jika belum ada
                            if w_indo not in self.word_dicts[lang]:
                                self.word_dicts[lang][w_indo] = w_local
                        else:
                            # Bangun kamus kata sederhana untuk kalimat utuh
                            indo_words = self.clean_text(indo_sent).split()
                            local_words = self.clean_text(local_sent).split()
                            
                            for i in range(min(len(indo_words), len(local_words))):
                                w_indo = indo_words[i]
                                w_local = local_words[i]
                                if w_indo not in self.word_dicts[lang]:
                                    self.word_dicts[lang][w_indo] = w_local
            print("Rule-Based Corpus loaded successfully!")
        except Exception as e:
            print(f"Gagal memuat corpus excel: {e}")

    def translate(self, text, source_lang, target_lang, register=None):
        import re
        # Penerjemahan hanya didukung dari/ke Indonesia untuk model kamus sederhana ini
        if source_lang == "Indonesia" and target_lang in self.sentence_dicts:
            lang = target_lang
            return self._translate_clauses(text, lang, register, reverse=False)
        elif target_lang == "Indonesia" and source_lang in self.sentence_dicts:
            lang = source_lang
            return self._translate_clauses(text, lang, register, reverse=True)
        else:
            return "Penerjemahan langsung antar bahasa daerah (misal Sunda -> Jawa) menggunakan model kamus tidak didukung. Silakan gunakan model Machine Learning."

    def _translate_clauses(self, text, lang, register, reverse=False):
        """Pecah input menjadi klausa per tanda baca, terjemahkan masing-masing."""
        import re
        parts = re.split(r'([,;.!?])', text.strip())
        result_parts = []
        for part in parts:
            stripped = part.strip()
            if not stripped:
                continue
            if re.match(r'^[,;.!?]$', stripped):
                result_parts.append(stripped)
            else:
                result_parts.append(self._translate_phrase(stripped, lang, register, reverse))
        result = ""
        for part in result_parts:
            if not result:
                result = part
            elif re.match(r'^[,;.!?]$', part):
                result += part
            else:
                result += " " + part
        return result

    def _translate_phrase(self, phrase, lang, register, reverse=False):
        """Terjemahkan satu frasa: exact match dulu, lalu word-by-word."""
        cleaned = phrase.strip().lower()
        if not reverse:
            # Indonesia -> Daerah: coba exact match dengan/tanpa register
            if register and f"{cleaned} ({register})" in self.sentence_dicts[lang]:
                return self.sentence_dicts[lang][f"{cleaned} ({register})"]
            if cleaned in self.sentence_dicts[lang]:
                return self.sentence_dicts[lang][cleaned]
            return self._word_by_word(phrase, lang, register)
        else:
            # Daerah -> Indonesia: balikkan sentence dict
            reverse_sent = {v.lower(): k for k, v in self.sentence_dicts[lang].items()}
            if cleaned in reverse_sent:
                r = reverse_sent[cleaned]
                return r.split(" (")[0].capitalize() if " (" in r else r.capitalize()
            reverse_words = {v.lower(): k for k, v in self.word_dicts[lang].items()}
            return self._word_by_word_reverse(phrase, reverse_words)

    def _word_by_word(self, phrase, lang, register):
        """Terjemahkan kata per kata dari Indonesia ke bahasa daerah."""
        import re
        tokens = re.findall(r"\w+|[^\w\s]", phrase)
        out = []
        for w in tokens:
            if not re.match(r'^\w+$', w):
                out.append(w); continue
            wl = w.lower()
            rw = None
            if register and f"{wl} ({register})" in self.word_dicts[lang]:
                rw = self.word_dicts[lang][f"{wl} ({register})"]
            if not rw and wl in self.word_dicts[lang]:
                rw = self.word_dicts[lang][wl]
            if not rw and f"{wl} (biasa)" in self.word_dicts[lang]:
                rw = self.word_dicts[lang][f"{wl} (biasa)"]
            if rw:
                if w.istitle(): rw = rw.title()
                elif w.isupper(): rw = rw.upper()
                out.append(rw)
            else:
                out.append(f"[{w}]")
        return self._join_tokens(out)

    def _word_by_word_reverse(self, phrase, reverse_word_dict):
        """Terjemahkan kata per kata dari bahasa daerah ke Indonesia."""
        import re
        tokens = re.findall(r"\w+|[^\w\s]", phrase)
        out = []
        for w in tokens:
            if not re.match(r'^\w+$', w):
                out.append(w); continue
            wl = w.lower()
            if wl in reverse_word_dict:
                rw = reverse_word_dict[wl]
                if " (" in rw: rw = rw.split(" (")[0]
                if w.istitle(): rw = rw.title()
                elif w.isupper(): rw = rw.upper()
                out.append(rw)
            else:
                out.append(f"[{w}]")
        return self._join_tokens(out)

    def _join_tokens(self, tokens):
        """Gabungkan token, tanda baca langsung menempel tanpa spasi."""
        result = ""
        for i, t in enumerate(tokens):
            if i == 0: result += t
            elif t in [",", ".", "!", "?", ";", ":"]: result += t
            else: result += " " + t
        return result

class MLTranslator:
    def __init__(self):
        self.pipeline = None
        self.model_loaded = False

    def load_model(self):
        if self.model_loaded:
            return True
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline
            import torch
            
            model_name = "facebook/nllb-200-distilled-600M"
            device = 0 if torch.cuda.is_available() else -1
            
            print("Mengunduh/Memuat model NLLB-200 (2.4 GB)... Ini bisa memakan waktu beberapa menit di awal.")
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            
            self.pipeline = pipeline(
                "translation",
                model=model,
                tokenizer=tokenizer,
                device=device
            )
            self.model_loaded = True
            print("Model NLLB-200 berhasil dimuat!")
            return True
        except Exception as e:
            print(f"Gagal memuat model Machine Learning: {e}")
            return False

    def translate(self, text, source_lang, target_lang):
        if not self.model_loaded:
            success = self.load_model()
            if not success:
                return "Error: Gagal memuat model Machine Learning. Pastikan pustaka transformers terinstal."
        
        src_code = NLLB_CODE_MAP.get(source_lang)
        tgt_code = NLLB_CODE_MAP.get(target_lang)
        
        if not src_code or not tgt_code:
            return f"Bahasa {source_lang} atau {target_lang} tidak didukung oleh model NLLB."
            
        try:
            result = self.pipeline(
                text,
                src_lang=src_code,
                tgt_lang=tgt_code,
                max_length=400
            )
            return result[0]['translation_text']
        except Exception as e:
            return f"Error saat menerjemahkan: {e}"
