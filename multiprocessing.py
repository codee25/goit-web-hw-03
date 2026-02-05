import argparse
import logging
from pathlib import Path
from shutil import copy2
from threading import Semaphore, Thread

# Налаштування логування
logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')

# Обмежуємо кількість одночасних потоків, щоб не перевантажити систему
pool = Semaphore(10)

def copy_file(file_path: Path, target_dir: Path):
    with pool:
        try:
            # Визначаємо підпапку за розширенням
            ext = file_path.suffix[1:].lower() or "no_extension"
            destination = target_dir / ext
            destination.mkdir(parents=True, exist_ok=True)
            
            copy2(file_path, destination / file_path.name)
        except Exception as e:
            logging.error(f"Помилка при копіюванні {file_path}: {e}")

def read_folder(source_dir: Path, target_dir: Path):
    threads = []
    try:
        for item in source_dir.iterdir():
            if item.is_dir():
                # Створюємо новий потік для кожної піддиректорії (рекурсія)
                th = Thread(target=read_folder, args=(item, target_dir))
                th.start()
                threads.append(th)
            elif item.is_file():
                # Створюємо потік для копіювання файлу
                th = Thread(target=copy_file, args=(item, target_dir))
                th.start()
                threads.append(th)
        
        # Чекаємо завершення всіх потоків у цій папці
        for th in threads:
            th.join()
            
    except Exception as e:
        logging.error(f"Помилка обробки директорії {source_dir}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Сортування файлів за розширенням")
    parser.add_argument("source", type=str, help="Шлях до вхідної папки")
    parser.add_argument("output", type=str, nargs="?", default="dist", help="Шлях до папки призначення (default: dist)")
    
    args = parser.parse_args()
    
    source = Path(args.source)
    output = Path(args.output)

    if not source.exists():
        print("Вихідна папка не існує.")
    else:
        read_folder(source, output)
        print(f"Сортування завершено! Результати у папці: {output.absolute()}")