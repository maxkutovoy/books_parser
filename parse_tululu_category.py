import argparse
import json
import os
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests

from book_services import check_for_redirect, get_book_info, download_txt, \
    download_image


def main():
    base_url = 'https://tululu.org'

    books_dir = 'books'
    images_dir = 'images'
    Path(books_dir).mkdir(parents=True, exist_ok=True)
    Path(images_dir).mkdir(parents=True, exist_ok=True)

    pages_count = 1

    for page_number in range(1, pages_count + 1):

        sifi_books_url = f'https://tululu.org/l55/{page_number}'
        sifi_books_response = requests.get(sifi_books_url)

        sifi_books_soup = BeautifulSoup(sifi_books_response.text, 'lxml')
        books_on_page = sifi_books_soup.find_all('table', class_='d_book')

        books_info = []

        for book in books_on_page:

            book_href = book.find('a')['href']
            book_id = book_href.replace('/b', '').replace('/', '')
            book_url = urljoin(base_url, book_href)

            download_url = f'https://tululu.org/txt.php'
            download_params = {
                'id': book_id
            }

            try:
                downloaded_book_response = requests.get(download_url,
                                                        download_params)
                downloaded_book_response.raise_for_status()
                check_for_redirect(downloaded_book_response)

                book = requests.get(book_url)
                book_soup = BeautifulSoup(book.text, 'lxml')
                book_info = get_book_info(book_soup)
                book_info['book_path'] = download_txt(
                    downloaded_book_response,
                    book_info['title'],
                    book_id,
                    books_dir,
                )

                book_info['img_src'] = download_image(
                    downloaded_book_response,
                    book_info['img_url'],
                    images_dir,
                )

                del book_info['img_url']
                books_info.append(book_info)

            except requests.HTTPError:
                pass

        with open('books_description.json', 'a',
                  encoding='utf8') as my_file:
            json.dump(books_info, my_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
