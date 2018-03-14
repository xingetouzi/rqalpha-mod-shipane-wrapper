from pathlib import Path

WORK_DIR = "."

__all__ = ["get_file"]


def get_file(path):
    abs_path = str(Path(WORK_DIR) / path)
    with open(abs_path, "rb") as f:
        return f.read()
