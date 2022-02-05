import json
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

    books_in_page = list(chunked(books, 10))

    for page_number, page in enumerate(books_in_page):

        books_in_columns = list(chunked(page, 2))
        pprint(books_in_columns)
        rendered_page = template.render(books=books_in_columns)

        filename = f'index{page_number}.html'
        filepath = os.path.join(pages_dir, filename)

        with open(filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)
        print(f"Сохранили {filepath}")


def on_reload():
    server = Server()

    server.watch('template.html', render_site)

    server.serve(root='.')


def main():
    render_site()
    on_reload()


if __name__ == '__main__':
    main()
