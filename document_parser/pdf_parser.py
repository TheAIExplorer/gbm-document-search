import fitz  # PyMuPDF
from .base_parser import BaseParser
from models.document import Document
import camelot
import tabula
import io
from PIL import Image
import pytesseract

class PdfParser(BaseParser):
    @BaseParser.handle_errors
    def extract_text(self, file_path: str) -> Document:
        metadata = self.extract_metadata(file_path)
        text = ''
        tables_text = ''
        ocr_text = ''
        # Try PyMuPDF first
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
                # Extract images and OCR them
                for img_index in range(len(page.get_images(full=True))):
                    xref = page.get_images(full=True)[img_index][0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image['image']
                    image = Image.open(io.BytesIO(image_bytes))
                    ocr_text += pytesseract.image_to_string(image)
        except Exception:
            # Fallback to pdfminer.six
            try:
                from pdfminer.high_level import extract_text as pdfminer_extract
                text = pdfminer_extract(file_path)
            except Exception:
                # Fallback to PyPDF2
                try:
                    import PyPDF2
                    with open(file_path, 'rb') as f:
                        reader = PyPDF2.PdfReader(f)
                        for page in reader.pages:
                            text += page.extract_text() or ''
                except Exception:
                    text = ''
        # Table extraction with camelot
        try:
            tables = camelot.read_pdf(file_path, pages='all')
            for table in tables:
                tables_text += table.df.to_string(index=False) + '\n'
        except Exception:
            pass
        # Table extraction with tabula-py
        try:
            tabula_tables = tabula.read_pdf(file_path, pages='all', multiple_tables=True)
            for table in tabula_tables:
                tables_text += str(table) + '\n'
        except Exception:
            pass
        # Combine all extracted content
        full_text = '\n'.join([text, tables_text, ocr_text])
        full_text = self.normalize_text(full_text)
        language = self.detect_language(full_text)
        preview = self.get_preview(full_text)
        summary = self.summarize_text(full_text)
        lemmatized = self.lemmatize_text(full_text)
        entities = self.extract_entities(full_text)
        metadata['tables_extracted'] = bool(tables_text)
        metadata['ocr_images_extracted'] = bool(ocr_text)
        metadata.update({
            'summary': summary,
            'lemmatized': lemmatized,
            'entities': entities
        })
        return Document(
            file_id=metadata.get('file_id', ''),
            filename=file_path,
            content=full_text,
            url=metadata.get('url', ''),
            metadata=metadata,
            language=language,
            preview=preview
        )
