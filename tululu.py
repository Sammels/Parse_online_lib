import os
import requests

from bs4 import BeautifulSoup as bs
from pathvalidate import sanitize_filename


def download_txt(url, filename, folder='books/'):
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

    filename = sanitize_filename(f"{filename}.txt")
    filepath = os.path.join(folder)
    if check_for_redirect(response) is not False:
        with open(f'{filepath}{filename}', 'wb') as file:
            file.write(response.content)


def create_download_directory():
    """Создает директорию куда для скачивания файлов."""
    try:
        os.makedirs("books/", exist_ok=True)
    except FileExistsError:
        print("Папка уже существует.")


def check_for_redirect(response):
    """
    Проверяет статус ответа, если не 200, то исключение.

    Args:
        response (str):

    :return: bool
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

    book_number = range(1, 10)
    for book in book_number:
        payload = {"id": book}
        url = f"https://tululu.org/b{book}/"
        book_download_url = f"https://tululu.org/txt.php?id={book}"

        response = requests.get(url, params=payload)
        response.raise_for_status()

        if check_for_redirect(response) is not False:
            soup = bs(response.text, "lxml")

            title_tag = (
                soup.find("body")
                .find("table", class_="tabs")
                .find("td", class_="ow_px_td")
                .find("h1")
            )

            split_book_info = title_tag.text.rsplit('::')
            book_name = ''.join(split_book_info[0]).replace('\xa0', '').strip(' ')

            #download_txt(book_download_url, f"{book}. {book_name}")

    img_url = 'https://tululu.org/b9/'
    response = requests.get(img_url)
    response.raise_for_status()
    soup = bs(response.text, 'lxml')
    img_book_tag = (
        soup.find("body")
        .find("table", class_="tabs")
        .find('table', class_='d_book')
        .find('td')
        .find('div', class_='bookimage')
        .find('img')['src']
    )
    print(img_book_tag)




if __name__ == '__main__':
    main()