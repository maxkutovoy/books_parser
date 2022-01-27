import os
from urllib.parse import urljoin, unquote, urlsplit

import requests
from pathvalidate import sanitize_filename


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_info(book_soup):
    title_tag = book_soup.find('h1')
    book_title, author = (text.strip() for text in title_tag.text.split('::'))

    img_path = book_soup.find(class_="bookimage").find('img')['src']
    img_url = (urljoin('https://tululu.org', img_path))

    comments_tag = book_soup.find_all('div', class_="texts")
    comments = [comment.find('span', class_='black').text for comment in
                comments_tag]

    genres_tag = book_soup.find('span', class_="d_book").find_all('a')
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


def download_txt(response, book_title, book_id, folder='books/'):
    filename = f'{sanitize_filename(book_title)}'
    filepath = os.path.join(folder, filename)
    with open(f'{filepath}.txt', 'w') as book:
        book.write(response.text)

    return f'{filepath}.txt'


def download_image(response, img_url, folder='images/'):
    parsed_url = urlsplit(img_url)
    filename = os.path.split(unquote(parsed_url.path))[1]
    filepath = os.path.join(folder, filename)
    with open(f'{filepath}', 'wb') as book:
        book.write(response.content)

    return filepath
