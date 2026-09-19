from dataclasses import dataclass, field
from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional

@dataclass
class Note:
    title: str
    content: str
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    last_modified_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = UUID(self.id)
