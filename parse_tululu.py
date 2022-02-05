import argparse
import os
from pathlib import Path

from bs4 import BeautifulSoup
import requests

from book_services import (
    check_for_redirect, get_book_info, save_book_text, save_book_image
)


def main():
    parser = argparse.ArgumentParser(
        description='Программа скачивает книги с сайта https://tululu.org')
    parser.add_argument('start_id', help='Начальная страница', nargs='?',
                        default=1, type=int)
    parser.add_argument('end_id', help='Конечная страница', nargs='?',
                        default=10, type=int)
    args = parser.parse_args()

    books_dir = 'books'
    images_dir = 'images'
    Path(books_dir).mkdir(parents=True, exist_ok=True)
    Path(images_dir).mkdir(parents=True, exist_ok=True)

    for book_id in range(args.start_id, args.end_id + 1):
        try:
            book_url = f'https://tululu.org/b{book_id}'
            download_url = f'https://tululu.org/txt.php'
            download_params = {
                'id': book_id
            }

            downloaded_book_response = requests.get(download_url,
                                                    download_params)
            downloaded_book_response.raise_for_status()
            check_for_redirect(downloaded_book_response)

            book_info_response = requests.get(book_url)
            book_info_response.raise_for_status()
            book_info_soup = BeautifulSoup(book_info_response.text, 'lxml')

            book_info = get_book_info(book_info_soup)
            save_book_text(downloaded_book_response, book_info['title'],
                           book_id, books_dir)
            save_book_image(book_info['img_url'],
                            images_dir)
            print(f'Название: {book_info["title"]}')
            print(f'Автор: {book_info["author"]}')
            print()
        except requests.HTTPError:
            pass


if __name__ == '__main__':
    main()
