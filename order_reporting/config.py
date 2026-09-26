from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReportConfig:
    input_path: Path
    output_dir: Path
