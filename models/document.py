# models/document.py
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Document:
    file_id: str
    filename: str
    content: str
    url: str
    metadata: Dict = field(default_factory=dict)
    language: Optional[str] = None
    preview: Optional[str] = None
