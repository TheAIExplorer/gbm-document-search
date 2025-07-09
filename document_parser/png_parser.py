import pytesseract
from PIL import Image, ImageOps
from .base_parser import BaseParser
from models.document import Document
import numpy as np

class PngParser(BaseParser):
    @BaseParser.handle_errors
    def extract_text(self, file_path: str) -> Document:
        metadata = self.extract_metadata(file_path)
        # Image preprocessing: convert to grayscale, binarize, resize
        image = Image.open(file_path)
        image = ImageOps.grayscale(image)
        # Binarization (Otsu's method)
        arr = np.array(image)
        threshold = arr.mean()  # Simple threshold, can use Otsu for better results
        binarized = Image.fromarray((arr > threshold).astype(np.uint8) * 255)
        # Resize if too large
        max_dim = 2000
        if max(image.size) > max_dim:
            scale = max_dim / max(image.size)
            new_size = tuple([int(x * scale) for x in image.size])
            binarized = binarized.resize(new_size, Image.ANTIALIAS)
        # OCR with bounding boxes and confidence
        ocr_data = pytesseract.image_to_data(binarized, output_type=pytesseract.Output.DICT)
        text = ' '.join([word for word, conf in zip(ocr_data['text'], ocr_data['conf']) if word.strip() and conf != '-1'])
        avg_conf = np.mean([int(conf) for conf in ocr_data['conf'] if conf != '-1']) if ocr_data['conf'] else 0
        bboxes = [
            {
                'text': word,
                'left': left,
                'top': top,
                'width': width,
                'height': height,
                'conf': conf
            }
            for word, left, top, width, height, conf in zip(
                ocr_data['text'], ocr_data['left'], ocr_data['top'], ocr_data['width'], ocr_data['height'], ocr_data['conf'])
            if word.strip() and conf != '-1'
        ]
        text = self.normalize_text(text)
        language = self.detect_language(text)
        preview = self.get_preview(text)
        summary = self.summarize_text(text)
        lemmatized = self.lemmatize_text(text)
        entities = self.extract_entities(text)
        metadata['ocr_avg_confidence'] = avg_conf
        metadata['ocr_bounding_boxes'] = bboxes
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
