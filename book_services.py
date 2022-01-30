import os
from urllib.parse import urljoin, unquote, urlsplit

import requests
from pathvalidate import sanitize_filename

from bs4 import BeautifulSoup


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_info(book_soup):
    title_tag = book_soup.select_one('h1')
    book_title, author = (text.strip() for text in title_tag.text.split('::'))

    img_path = book_soup.select_one('.bookimage img')['src']
    img_url = (urljoin('https://tululu.org', img_path))

    comments_tag = book_soup.select('div.texts span.black')
    comments = [comment.text for comment in comments_tag]

    genres_tag = book_soup.select('span.d_book a')
    genres = [genre.text for genre in genres_tag]

    book_info = {
        'title': book_title,
        'author': author,
        'img_src': '',
        'book_path': '',
        'img_url': img_url,
        'comments': comments,
        'genres': genres,
    }
    return book_info


def get_category_last_page_number(base_url, category):
    try:
        category_url = urljoin(base_url, category)
        category_start_page_response = requests.get(category_url)
        category_start_page_response.raise_for_status()
        check_for_redirect(category_start_page_response)
    except requests.HTTPError:
        print('Нет такой категории, попробуй другую')
        exit()

    category_start_page_soup = BeautifulSoup(
        category_start_page_response.text,
        'lxml'
    )
    category_last_page_number = category_start_page_soup.select('p.center a')[-1].text
    return int(category_last_page_number)


def save_book_text(response, book_title, book_id, folder='books/'):
    filename = f'{sanitize_filename(book_title)}'
    filepath = os.path.join(folder, filename)
    with open(f'{filepath}.txt', 'w') as book:
        book.write(response.text)

    return f'{filepath}.txt'


def save_book_image(response, img_url, folder='images/'):
    parsed_url = urlsplit(img_url)
    filename = os.path.split(unquote(parsed_url.path))[1]
    filepath = os.path.join(folder, filename)
    with open(f'{filepath}', 'wb') as book:
        book.write(response.content)

    return filepath
