import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def copy_file(src_path, dest_dir):
    ext = src_path.suffix[1:].lower() or "no_ext"
    target_dir = dest_dir / ext
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, target_dir / src_path.name)


def process_directory(src_dir, dest_dir, executor):
    futures = []
    for entry in src_dir.iterdir():
        if entry.is_file():
            futures.append(executor.submit(copy_file, entry, dest_dir))
        elif entry.is_dir():
            futures.append(
                executor.submit(process_directory, entry, dest_dir, executor)
            )
    return futures


def main():
    if len(sys.argv) < 2:
        print("Usage: python sorter.py <source_dir> [<dest_dir>]")
        sys.exit(1)
    src_dir = Path(sys.argv[1])
    dest_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("dist")
    if not src_dir.exists() or not src_dir.is_dir():
        print(f"Source directory {src_dir} does not exist or is not a directory.")
        sys.exit(1)
    dest_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor() as executor:
        futures = process_directory(src_dir, dest_dir, executor)
        for future in as_completed(futures):
            pass  # All work is done in threads, no result needed
    print(f"Files from {src_dir} have been sorted into {dest_dir}")


if __name__ == "__main__":
    main()
