import os
from abc import ABC, abstractmethod
from typing import Dict, Optional
import chardet
from langdetect import detect, LangDetectException
import unicodedata
import nltk
import spacy
from nltk.corpus import stopwords

# Ensure NLTK stopwords are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load spaCy model (English for now)
try:
    nlp = spacy.load('en_core_web_sm')
except OSError:
    from spacy.cli import download
    download('en_core_web_sm')
    nlp = spacy.load('en_core_web_sm')

class BaseParser(ABC):
    @abstractmethod
    def extract_text(self, file_path: str) -> str:
        pass

    @staticmethod
    def detect_encoding(file_path: str) -> str:
        try:
            with open(file_path, 'rb') as f:
                raw = f.read(4096)
            result = chardet.detect(raw)
            return result['encoding'] or 'utf-8'
        except Exception:
            return 'utf-8'

    @staticmethod
    def extract_metadata(file_path: str) -> Dict:
        try:
            stat = os.stat(file_path)
            return {
                'size': stat.st_size,
                'created': stat.st_ctime,
                'modified': stat.st_mtime
            }
        except Exception:
            return {}

    @staticmethod
    def detect_language(text: str) -> Optional[str]:
        try:
            return detect(text)
        except (LangDetectException, Exception):
            return None

    @staticmethod
    def normalize_text(text: str) -> str:
        # Unicode normalization, strip, collapse whitespace
        text = unicodedata.normalize('NFKC', text)
        text = ' '.join(text.split())
        return text

    @staticmethod
    def get_preview(text: str, n: int = 200) -> str:
        return text[:n] + ('...' if len(text) > n else '')

    @staticmethod
    def handle_errors(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return f"[ERROR] {str(e)}"
        return wrapper

    @staticmethod
    def remove_stopwords(text: str, lang: str = 'english') -> str:
        stop_words = set(stopwords.words(lang))
        return ' '.join([word for word in text.split() if word.lower() not in stop_words])

    @staticmethod
    def lemmatize_text(text: str) -> str:
        doc = nlp(text)
        return ' '.join([token.lemma_ for token in doc])

    @staticmethod
    def summarize_text(text: str, max_sentences: int = 2) -> str:
        doc = nlp(text)
        sentences = list(doc.sents)
        return ' '.join([sent.text for sent in sentences[:max_sentences]])

    @staticmethod
    def extract_entities(text: str) -> Dict:
        doc = nlp(text)
        entities = [{'text': ent.text, 'label': ent.label_} for ent in doc.ents]
        return {'entities': entities}
