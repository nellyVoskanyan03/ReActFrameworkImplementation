from pathlib import Path

PROMPT_TEMPLATE_PATH = Path(__file__).parent / "prompt.txt"


def read_file(path: Path) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as file:
            content: str = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {path}")
        return None
    except Exception as e:
        print(f"Error reading file {path}: {e}")
        return None


def get_template() -> str:
    return read_file(PROMPT_TEMPLATE_PATH)
