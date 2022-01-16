import argparse
import os
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


def get_books():
    base_url = 'https://tululu.org'

    pages_count = 10
    for page_number in range(1, pages_count+1):
        print(f'Page: {page_number}')
        print('Books:')
        sifi_books_url = f'https://tululu.org/l55/{page_number}'
        sifi_books_response = requests.get(sifi_books_url)

        sifi_books_soup = BeautifulSoup(sifi_books_response.text, 'lxml')
        books_on_page = sifi_books_soup.find_all('table', class_='d_book')
        for book in books_on_page:
            book_href = book.find('a')['href']
            book_url = urljoin(base_url, book_href)
            print(book_url)


get_books()
