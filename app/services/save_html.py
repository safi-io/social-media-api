import uuid
from pathlib import Path

BASE_DIR = Path("generated_sites")
BASE_DIR.mkdir(exist_ok=True)


def save_generated_html(html_content: str):
    file_id = uuid.uuid4().hex
    file_path = BASE_DIR / f"{file_id}.html"

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return file_id
