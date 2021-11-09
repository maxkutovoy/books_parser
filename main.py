import os
from pathlib import Path
from pprint import pprint
from urllib.parse import urljoin, unquote, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def download_book(image_dir, book_id):
    url = f'https://tululu.org/txt.php?id={book_id}'

    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)

    with open(f'{image_dir}/book{book_id}.txt', 'w') as book:
        book.write(response.text)


def download(url, filename, folder='Books/'):
    """Функция для скачивания текстовых файлов.
    Args:
        url (str): Cсылка на текст, который хочется скачать.
        filename (str): Имя файла, с которым сохранять.
        folder (str): Папка, куда сохранять.
    Returns:
        str: Путь до файла, куда сохранён текст.
    """


def get_book_info(book_id):
    url = f'https://tululu.org/b{book_id}'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'lxml')
    title_tag = soup.find('h1')
    title_text = title_tag.text
    try:
        book_title, author = title_text.split('   ::   ')
    except ValueError:
        return None, None
    img = soup.find(class_="bookimage").find('img')['src']
    img_url = (urljoin('https://tululu.org', img))
    try:
        comments = soup.find_all('div', class_="texts")
        for comment in comments:
            c = comment.find('span', class_='black')
            print(f'Комментарий: {c.text}')
    except:
        pass
    return book_title, img_url


def download_txt(id, book_title, folder='books/'):
    url = f'https://tululu.org/txt.php?id={id}'
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    print(book_title)
    filename = f'{id}. {sanitize_filename(book_title)}'
    filepath = os.path.join(folder, filename)
    with open(f'{filepath}.txt', 'w') as book:
        book.write(response.text)


def download_image(url, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    parsed_url = urlsplit(url)
    filename = os.path.split(unquote(parsed_url.path))[1]
    filepath = os.path.join(folder, filename)
    with open(f'{filepath}', 'wb') as book:
        book.write(response.content)


if __name__ == '__main__':
    books_dir = 'books'
    images_dir = 'images'
    Path(books_dir).mkdir(parents=True, exist_ok=True)
    Path(images_dir).mkdir(parents=True, exist_ok=True)
    for book_id in range(1, 11):
        try:
            book_title, img_url = get_book_info(book_id)
            if book_title is not None:
                download_txt(book_id, book_title, books_dir)
                download_image(img_url, folder='images/')
        except requests.HTTPError:
            pass


