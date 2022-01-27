import argparse


def create_parser():
    parser = argparse.ArgumentParser(
        description='Программа скачивает книги с сайта https://tululu.org' \
                    'из категории "Научная фантастика"')

    parser.add_argument(
        'start_page',
        help='Начальная страница',
        nargs='?',
        default=1,
        type=int,
    )

    parser.add_argument(
        'end_page',
        help='Конечная страница',
        nargs='?',
        type=int,
    )

    parser.add_argument(
        '--dest_folder',
        help='Показывает путь к каталогу с результатами парсинга',
        action='store_true',
        default=False,
    )

    parser.add_argument(
        '--skip_imgs',
        help=(
            'Параметр отвечающий за пропуск скачивания'
            'фотографий при парсинге'
        ),
        action='store_true',
        default=False,
    )

    parser.add_argument(
        '--skip_txt',
        help=(
            'Параметр отвечающий за пропуск скачивания'
            'текста книги при парсинге'
        ),
        action='store_true',
        default=False,
    )

    parser.add_argument(
        '--json_path',
        help=(
            'Параметр отвечающий за путь сохранения *.json файла'
            'с описанием скачанных книг'
        ),
        default='.',
    )

    return parser
