import os
from .txt_parser import TxtParser
from .csv_parser import CsvParser
from .pdf_parser import PdfParser
from .png_parser import PngParser
from .base_parser import BaseParser

class ParserFactory:
    def get_parser(self, file_path: str) -> BaseParser:
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.txt':
            return TxtParser()
        elif ext == '.csv':
            return CsvParser()
        elif ext == '.pdf':
            return PdfParser()
        elif ext == '.png':
            return PngParser()
        else:
            raise ValueError(f"Unsupported file type: {ext}")
