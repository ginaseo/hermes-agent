import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "HermesVault" / "index"


class ProcessingState:

    def __init__(self, name: str, force: bool = False):
        STATE_DIR.mkdir(parents=True, exist_ok=True)
        self.force = force
        self.file = STATE_DIR / f"{name}_state.json"
        self.state: dict[str, float] = {}
        if self.file.exists():
            self.state = json.loads(self.file.read_text(encoding="utf-8"))

    def is_modified(self, file: Path) -> bool:
        if self.force:
            return True
        key = str(file.resolve())
        return self.state.get(key) != file.stat().st_mtime

    def update(self, file: Path) -> None:
        self.state[str(file.resolve())] = file.stat().st_mtime

    def save(self) -> None:
        self.file.write_text(
            json.dumps(self.state, ensure_ascii=False, indent=4),
            encoding="utf-8",
        )
