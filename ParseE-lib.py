import requests
import os
from pathlib import Path

def download_books_txt():
    """Скачивает книги в txt формате."""
    books = range(1, 10)

    for book in books:
        url = f"https://tululu.org/txt.php?id={book}"

        response = requests.get(url)
        response.raise_for_status()

        with open(f'books/id{book}.txt', 'wb') as file:
            file.write(response.content)

def create_download_directory():
    try:
        os.makedirs("/home/sammels/Документы/Work/Devman/DevmanCourse_week28/ParseOnlineLib/books/", exist_ok=True)
    except FileExistsError:
        pass
def main():
    """Запускает исполнение скрипта."""
    create_download_directory()
    download_books_txt()


if __name__ == "__main__":
    main()
