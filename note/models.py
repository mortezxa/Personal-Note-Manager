from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4


@dataclass
class Note:
    title: str
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at = field(default_factory=datetime.now)
