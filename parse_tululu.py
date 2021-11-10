import argparse
import os
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_info(book_soup):
    title_tag = book_soup.find('h1')
    title_text = title_tag.text
    book_title, author = title_text.split('   ::   ')

    img_path = book_soup.find(class_="bookimage").find('img')['src']
    img_url = (urljoin('https://tululu.org', img_path))

    comments_tag = book_soup.find_all('div', class_="texts")
    comments = [comment.find('span', class_='black').text for comment in comments_tag]

    genres_tag = book_soup.find('span', class_="d_book").find_all('a')
    genres = [genre.text for genre in genres_tag]

    book_info = {
        'book_title': book_title,
        'author': author,
        'img_url': img_url,
        'comments': comments,
        'genres': genres,
    }
    return book_info


def download_txt(response, book_title, book_id, folder='books/'):
    filename = f'{book_id}. {sanitize_filename(book_title)}'
    filepath = os.path.join(folder, filename)
    with open(f'{filepath}.txt', 'w') as book:
        book.write(response.text)


def download_image(response, img_url, folder='images/'):
    parsed_url = urlsplit(img_url)
    filename = os.path.split(unquote(parsed_url.path))[1]
    filepath = os.path.join(folder, filename)
    with open(f'{filepath}', 'wb') as book:
        book.write(response.content)


def main():
    parser = argparse.ArgumentParser(description='Программа скачивает с сайта https://tululu.org')
    parser.add_argument('start_id', help='Начальная страница', nargs='?', default=1, type=int)
    parser.add_argument('end_id', help='Конечная страница', nargs='?', default=10, type=int)
    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id

    books_dir = 'books'
    images_dir = 'images'
    Path(books_dir).mkdir(parents=True, exist_ok=True)
    Path(images_dir).mkdir(parents=True, exist_ok=True)

    for book_id in range(start_id, end_id + 1):
        try:
            book_url = f'https://tululu.org/b{book_id}'
            download_url = f'https://tululu.org/txt.php?id={book_id}'

            download_page = requests.get(download_url)
            download_page.raise_for_status()
            check_for_redirect(download_page)

            book_page = requests.get(book_url)
            book_page.raise_for_status()
            book_page = BeautifulSoup(book_page.text, 'lxml')

            book_info = get_book_info(book_page)
            download_txt(download_page, book_info['book_title'], book_id, books_dir)
            download_image(download_page, book_info['img_url'], images_dir)
            print(f'Название: {book_info["book_title"]}')
            print(f'Автор: {book_info["author"]}')
            print()
        except requests.HTTPError:
            pass


if __name__ == '__main__':
    main()
