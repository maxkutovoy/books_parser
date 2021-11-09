from pathlib import Path

import requests


def download_book(image_dir):
    url = 'https://tululu.org/txt.php?id=32168'

    response = requests.get(url)
    response.raise_for_status()

    with open(f'{image_dir}/book.txt', 'w') as book:
        book.write(response.text)


if __name__ == '__main__':
    image_dir = 'Books'
    Path(image_dir).mkdir(parents=True, exist_ok=True)
    download_book(image_dir)


