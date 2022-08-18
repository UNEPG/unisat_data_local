from pathlib import Path


def get_home_dir() -> Path:
    home_dir = Path.home()
    return home_dir


def create_file_if_not_exists(file_name: str) -> bool:
    home_dir = get_home_dir()
    dir_path = Path(home_dir / "unisat")
    file = dir_path / f"{file_name}"
    dir_path.mkdir(exist_ok=True, parents=True)
    file.touch(exist_ok=True)
    return True
