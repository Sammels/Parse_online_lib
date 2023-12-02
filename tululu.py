import os
import time
from time import time
import argparse
import requests

from urllib.parse import urljoin
from pathvalidate import sanitize_filename
from bs4 import BeautifulSoup as bs


def parse_book_page(html_content) -> dict:
    """Принимает html страницы и возвращает словарь.

        book_information = {'title': f"Заголовок: {book_name}",
                "genre": genre,
                "book_image_url": img_url,
                "img_ext": extension,
                "comments": book_comments,
                }

    Args:
        html_content (str): Сырой HTML код страницы.

    Returns:
        dict: Словарь содержащий данные книги.

    """
    title_tag = (
        html_content.find("body")
        .find("table", class_="tabs")
        .find("td", class_="ow_px_td")
        .find("h1")
    )
    split_book = title_tag.text.rsplit("::")
    book_name = "".join(split_book[0]).replace("\xa0", "").strip(" ")

    img_book_tag = (
        html_content.find("body")
        .find("div", class_="bookimage")
        .find("img")["src"]
    )
    extension = list(img_book_tag)[-4:]
    extension = "".join(extension)
    img_url = urljoin("https://tululu.org", img_book_tag)

    comments_book_tag = (
        html_content.find("body")
        .find("table", class_="tabs")
        .find("td", class_="ow_px_td")
        .find_all("span", class_="black")
    )
    comments = comments_book_tag
    com = [comments[x].text for x, y in enumerate(comments) if len(comments) > 0]
    book_comments = [coms for coms in com]

    genre_book_tag = html_content.find("body").find("span", class_="d_book")
    genre_book = genre_book_tag.find_all("a")

    genre = [x.text for x in genre_book]

    book_information = {
        "title": f"Заголовок: {book_name}",
        "genre": genre,
        "book_image_url": img_url,
        "img_ext": extension,
        "comments": book_comments,
    }
    return book_information


def download_txt(url, params, filename, folder="books/"):
    """Функция для скачивания текстовых файлов.

    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.

    Returns:
        str: Путь до файла, куда сохранён текст.
    """
    response = requests.get(url, params=params)
    response.raise_for_status()

    filename = sanitize_filename(f"{filename}.txt")
    filepath = os.path.join(folder)
    if check_for_redirect(response) is not False:
        with open(f"{filepath}{filename}", "wb") as file:
            file.write(response.content)


def download_images(url, filename, folder="images/"):
    """Функция для скачивания текстовых файлов.

    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.

    Returns:
        str: Путь до файла, куда сохранён текст.
    """

    response = requests.get(url)
    response.raise_for_status()

    with open(f"images/{filename}", "wb") as file:
        file.write(response.content)


def create_download_directory():
    """Создает директорию куда для скачивания файлов."""
    os.makedirs("books/", exist_ok=True)
    os.makedirs("images/", exist_ok=True)


def check_for_redirect(response):
    """
    Проверяет статус ответа, если не 200, то исключение.

    Args:
        response (str):

    Returns:
         bool
    """
    try:
        if len(response.history) > 0:
            if response.history[0].status_code == 200:
                pass
            else:
                raise requests.exceptions.HTTPError

    except requests.exceptions.HTTPError:
        return False


def main():
    """Запускает скрипт."""
    parser = argparse.ArgumentParser(
        description="Программа парсит и скачивает данные книги с сайта"
    )
    parser.add_argument(
        "-start_id",
        "--start_page",
        type=int,
        default=1,
        help="Откуда стартует индекс книги",
    )
    parser.add_argument(
        "-end_id", "--end_page", type=int, default=10, help="Окончание индекса"
    )
    args = parser.parse_args()

    create_download_directory()

    book_index = range(args.start_page, args.end_page)
    for book_id in book_index:
        payload = {"id": book_id}
        url = f"https://tululu.org/b{book_id}/"
        book_download_url = f"https://tululu.org/txt.php"

        try:
            response = requests.get(url, params=payload)
            response.raise_for_status()

            if check_for_redirect(response) is not False:
                soup = bs(response.text, "lxml")
                parsed_book_page = parse_book_page(soup)
                download_txt(
                    book_download_url,
                    payload,
                    f"{book_id}. {parsed_book_page['title']}",
                )
                download_images(
                    parsed_book_page["book_image_url"],
                    f"{book_id}{parsed_book_page['img_ext']}",
                )
        except requests.exceptions.HTTPError:
            print("Ошибка запроса.")
        except requests.exceptions.ConnectionError:
            print("Проблемы с соединением.")
            time.sleep(25)


if __name__ == "__main__":
    work_time = time()
    main()
    now_time = time() - work_time
    print(now_time)
