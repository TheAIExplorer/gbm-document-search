from .base_parser import BaseParser
from models.document import Document

class TxtParser(BaseParser):
    @BaseParser.handle_errors
    def extract_text(self, file_path: str) -> Document:
        encoding = self.detect_encoding(file_path)
        metadata = self.extract_metadata(file_path)
        with open(file_path, 'r', encoding=encoding, errors='ignore') as f:
            text = f.read()
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
