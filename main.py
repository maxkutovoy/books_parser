from pathlib import Path
from pprint import pprint

from bs4 import BeautifulSoup
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


def book_parser():
    url = 'https://tululu.org/b1/'

    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    # pprint(soup.prettify())
    title_tag = soup.find('h1')
    title_text = title_tag.text
    book_title, author = title_text.split('   ::   ')
    print(f'Название книги: {book_title}')
    print(f'Автор: {author}')

    img = soup.find(class_="bookimage").find('img')['src']
    print(img)


if __name__ == '__main__':
    image_dir = 'Books'
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    # for book_id in range(1, 11):
    #     try:
    #         download_book(image_dir, book_id)
    #     except requests.HTTPError:
    #         pass
    book_parser()


