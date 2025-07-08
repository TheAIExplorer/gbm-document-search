import pandas as pd
from .base_parser import BaseParser

class CsvParser(BaseParser):
    def extract_text(self, file_path: str) -> str:
        df = pd.read_csv(file_path, dtype=str, encoding='utf-8', error_bad_lines=False)
        return ' '.join(df.fillna('').astype(str).values.flatten())
