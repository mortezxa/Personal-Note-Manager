from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Note:
    title: str
    content: str
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=_utc_now)
    updated_at: datetime = field(default_factory=_utc_now)

    def __post_init__(self) -> None:
        if isinstance(self.id, UUID):
            self.id = str(self.id)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(self.updated_at)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": str(self.id),
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Note":
        updated = data.get("updated_at") or data.get("last_modified_at")
        return cls(
            id=str(data.get("id", uuid4())),
            title=str(data["title"]),
            content=str(data["content"]),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if isinstance(data.get("created_at"), str)
                else _utc_now()
            ),
            updated_at=(
                datetime.fromisoformat(updated)
                if isinstance(updated, str)
                else _utc_now()
            ),
        )