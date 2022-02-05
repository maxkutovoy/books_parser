from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

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

