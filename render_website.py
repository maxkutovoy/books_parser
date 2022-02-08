import json
import math
import os
from pathlib import Path
from pprint import pprint

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def render_site():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    pages_dir = 'pages'
    Path(pages_dir).mkdir(parents=True, exist_ok=True)
    with open("books_description.json", "r") as my_file:
        books = json.load(my_file)

    books_in_page_count = 10
    books_in_page = list(chunked(books, books_in_page_count))
    pages_count = math.ceil(len(books)/books_in_page_count)
    print(pages_count)

    for page_number, page in enumerate(books_in_page, start=1):
        filename = f'index{page_number}.html'
        filepath = os.path.join(pages_dir, filename)
        books_in_columns = list(chunked(page, 2))

        rendered_page = template.render(
            {
                'books': books_in_columns,
                'pages_count': pages_count,
                'current_page': page_number,
            }
        )

        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def on_reload():
    server = Server()

    server.watch('template.html', render_site)

    server.serve(root='.')


def main():
    render_site()
    on_reload()


if __name__ == '__main__':
    main()
