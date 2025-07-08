from .base_parser import BaseParser

class TxtParser(BaseParser):
    def extract_text(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
