import pandas as pd
import csv
from .base_parser import BaseParser
from models.document import Document

class CsvParser(BaseParser):
    @BaseParser.handle_errors
    def extract_text(self, file_path: str) -> Document:
        encoding = self.detect_encoding(file_path)
        metadata = self.extract_metadata(file_path)
        # Delimiter detection
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            sample = f.read(2048)
            sniffer = csv.Sniffer()
            delimiter = ','
            try:
                delimiter = sniffer.sniff(sample).delimiter
            except Exception:
                pass
        try:
            df = pd.read_csv(file_path, dtype=str, encoding=encoding, delimiter=delimiter, on_bad_lines='skip')
            text = ' '.join(df.fillna('').astype(str).values.flatten())
        except Exception:
            text = ''
        text = self.normalize_text(text)
        language = self.detect_language(text)
        preview = self.get_preview(text)
        summary = self.summarize_text(text)
        lemmatized = self.lemmatize_text(text)
        entities = self.extract_entities(text)
        metadata.update({
            'summary': summary,
            'lemmatized': lemmatized,
            'entities': entities
        })
        return Document(
            file_id=metadata.get('file_id', ''),
            filename=file_path,
            content=text,
            url=metadata.get('url', ''),
            metadata=metadata,
            language=language,
            preview=preview
        )
