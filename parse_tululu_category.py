import argparse
import os
from pathlib import Path
from urllib.parse import urljoin, unquote, urlsplit

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests


def get_books():
    base_url =  'https://tululu.org'
    sifi_books_url = 'https://tululu.org/l55/'
    sifi_books_response = requests.get(sifi_books_url)

    sifi_books_soup = BeautifulSoup(sifi_books_response.text, 'lxml')
    book = sifi_books_soup.find('table', class_='d_book').find('a')

    book_url = urljoin(base_url, book['href'])

    print(book_url)


get_books()
