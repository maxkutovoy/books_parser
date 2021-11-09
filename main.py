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


def get_book_info(book_soup):
    title_tag = book_soup.find('h1')
    title_text = title_tag.text
    book_title, author = title_text.split('   ::   ')
    return book_title, author


def get_image_url(book_soup):
    img = book_soup.find(class_="bookimage").find('img')['src']
    img_url = (urljoin('https://tululu.org', img))
    return img_url


def get_comments(book_soup):
    comments_tag = book_soup.find_all('div', class_="texts")
    comments = [comment.find('span', class_='black').text for comment in comments_tag]
    return comments


def get_genre(book_soup):
    genres_tag = book_soup.find('span', class_="d_book").find_all('a')
    genres = [genre.text for genre in genres_tag]
    return genres


def download_txt(url, book_title, folder='books/'):
    response = requests.get(url)
    response.raise_for_status()
    print(book_title)
    filename = f'{id}. {sanitize_filename(book_title)}'
    filepath = os.path.join(folder, filename)
    # with open(f'{filepath}.txt', 'w') as book:
    #     book.write(response.text)


def download_image(url, folder='images/'):
    response = requests.get(url)
    response.raise_for_status()
    parsed_url = urlsplit(url)
    filename = os.path.split(unquote(parsed_url.path))[1]
    filepath = os.path.join(folder, filename)
    # with open(f'{filepath}', 'wb') as book:
    #     book.write(response.content)


if __name__ == '__main__':
    books_dir = 'books'
    images_dir = 'images'
    Path(books_dir).mkdir(parents=True, exist_ok=True)
    Path(images_dir).mkdir(parents=True, exist_ok=True)
    for book_id in range(1, 11):
        try:
            book_url = f'https://tululu.org/b{book_id}'
            download_url = f'https://tululu.org/txt.php?id={book_id}'

            response = requests.get(download_url)
            response.raise_for_status()
            check_for_redirect(response)

            response = requests.get(book_url)
            response.raise_for_status()
            book_soup = BeautifulSoup(response.text, 'lxml')

            book_title, author = get_book_info(book_soup)
            img_url = get_image_url(book_soup)
            # download_txt(download_url, book_title, books_dir)
            # download_image(img_url, folder='images/')
            get_comments(book_soup)
            # get_genre(book_soup)

        except requests.HTTPError:
            pass


