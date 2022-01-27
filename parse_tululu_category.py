import json
import os
from itertools import count
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

from bs4 import BeautifulSoup
import requests

from book_services import (
    check_for_redirect, get_book_info, save_book_text, save_book_image
)

from arguments import create_parser
from book_services import get_last_category_page


def main():
    parser = create_parser()

    base_url = 'https://tululu.org'
    download_url = urljoin(base_url, 'txt.php')
    category = 'l55/'

    last_category_page = get_last_category_page(base_url, category)

    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page

    books_dir = 'books'
    images_dir = 'images'
    Path(books_dir).mkdir(parents=True, exist_ok=True)
    Path(images_dir).mkdir(parents=True, exist_ok=True)

    if not end_page or end_page > last_category_page:
        end_page = last_category_page
        print(
            f'В данной категории всего {last_category_page}'
            'страниц, качаем все'
        )

    books_info = []

    for page_number in range(start_page, end_page+1):
        try:
            category_page = f'{category}/{page_number}'
            category_books_url = urljoin(base_url, category_page)
            category_books_response = requests.get(category_books_url)
            category_books_response.raise_for_status()
            check_for_redirect(category_books_response)

            category_books_soup = BeautifulSoup(
                category_books_response.text,
                'lxml'
            )
            books_on_page = category_books_soup.select('table.d_book')

        except requests.HTTPError:
            print('Страница не найдена, идем на следующую')

        for book in books_on_page:

            book_href = book.select_one('a')['href']
            book_id = book_href.replace('/b', '').replace('/', '')
            book_url = urljoin(base_url, book_href)

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

                if args.skip_txt:
                    book_info['book_path'] = ''
                else:
                    book_info['book_path'] = save_book_text(
                        downloaded_book_response,
                        book_info['title'],
                        book_id,
                        books_dir,
                    )

                if args.skip_imgs:
                    book_info['img_src'] = ''
                else:
                    book_info['img_src'] = save_book_image(
                        downloaded_book_response,
                        book_info['img_url'],
                        images_dir,
                    )
                    del book_info['img_url']

                books_info.append(book_info)
                print(f'Название: {book_info["title"]}')
                print(f'Автор: {book_info["author"]}')
                print()

            except requests.HTTPError:
                pass

    print('Все скачали')

    Path(args.json_path).mkdir(parents=True, exist_ok=True)
    path = f'{args.json_path}/books_description.json'

    with open(path, 'a', encoding='utf8') as books_db:
        json.dump(
            books_info,
            books_db,
            indent=4,
            ensure_ascii=False
        )

    if args.dest_folder:
        path = Path("parser_tululu_category.py").resolve()
        path_to_books = os.path.join(path.parent, books_dir)
        path_to_images = os.path.join(path.parent, images_dir)
        print(
            'Родительский каталог проекта (там по умолчанию  лежит json файл '
            'с информацией о скаченных книгах):'
            f'\n{path.parent}\n'
        )
        print(
            'Книги находятся в каталоге:'
            f'\n{path_to_books}\n'
        )
        print(
            'Обложки к книгам находятся в каталоге:'
            f'\n{path_to_images}\n'
        )


if __name__ == '__main__':
    main()
