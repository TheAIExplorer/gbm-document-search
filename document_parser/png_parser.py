import pytesseract
from PIL import Image
from .base_parser import BaseParser

class PngParser(BaseParser):
    def extract_text(self, file_path: str) -> str:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
