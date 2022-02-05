from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
from livereload import Server, shell


def render_site():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open("books_description.json", "r") as my_file:
        books = json.load(my_file)

    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print("Обновили HTML")


def on_reload():
    server = Server()

    server.watch('template.html', render_site)

    server.serve(root='.')


def main():
    render_site()
    on_reload()


if __name__ == '__main__':
    main()
