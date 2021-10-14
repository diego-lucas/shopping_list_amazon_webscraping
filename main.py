import pandas as pd
from utils import make_request
from parse import parse_html
from pg_upload import insert_database


def main():

    # url = "https://www.amazon.com.br/hz/wishlist/ls/UV6W7D39BZOS"
    url = "https://www.amazon.com.br/hz/wishlist/ls/3A4REEY8Q5T4G"

    html_content = make_request(url)
    data = parse_html(html_content)

    columns = (
        "title", "price", "image", "link", "author", "book_type", "review", "price_dropped"
    )

    insert_database(
        database = "amazon",
        table = "shopping_list.books",
        data = data,
        columns = columns
    )


if __name__ == "__main__":
    main()
