# models/document.py
from dataclasses import dataclass

@dataclass
class Document:
    file_id: str
    filename: str
    content: str
    url: str
