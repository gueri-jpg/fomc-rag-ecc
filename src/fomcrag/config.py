"""Explicit project paths; no automatic .env or benchmark loading."""
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    root: Path

    @property
    def pdfs(self) -> Path:
        return self.root / "utils" / "TxtExtraction" / "TextsData"

    @property
    def artifacts(self) -> Path:
        return self.root / "artifacts"

    @classmethod
    def from_root(cls, root: str | Path) -> "ProjectPaths":
        path = Path(root).resolve()
        if not (path / "configs" / "experiment_protocol.json").is_file():
            raise ValueError("Project root must contain configs/experiment_protocol.json")
        return cls(path)
