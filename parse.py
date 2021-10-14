import json
from bs4 import BeautifulSoup as soup
from utils import make_request


def parse_html(html: bytes, data_final: list = []) -> list:
    """
        Faz os tratamentos para que possa extrair informações do html da página.
        Retorna uma lista de tuplas, onde cada tupla representa um livro.
    """

    # Cria um objeto do BeautifulSoup para podermos tratar o html
    content_soup = soup(html, "lxml")

    # Cria um iterável com todos livros
    books = content_soup.find("ul", {"id": "g-items"}).find_all("li")

    for book in books:
        # Faz o tratamento de cada livro, para obtermos uma tupla com as informações formatadas
        row = parse_book(book)
        # Adiciona a tupla a uma lista final
        data_final.append(row)

    print("Tamanho do vetor:", len(data_final))

    # Checa se possui uma proxima pagina
    next_page_url = check_next_page(content_soup)

    if next_page_url:
        # Em caso positivo, faz a requisicao a url da nova página
        next_page_html = make_request(next_page_url)
        # Faz o tratamento da nova página chamando a função de forma recursiva
        parse_html(next_page_html, data_final)

    # Retorna a lista de tuplas que contém os dados
    return data_final

def parse_book(book_html: soup) -> tuple:
    """
        Recebe como parâmetro o html de um livro.
        Faz todas as transformações para que os dados fiquem padronizados.
        Retorna um tupla com as informações do livro.
    """

    # O titulo do livro é a tag h3
    title = book_html.find("h3").text.strip()

    price = None
    # Checa se o livro está disponível
    if book_html.find("span", {"class": "a-price"}):
        # Caso positivo, busca pelo preco e subsitui a ',' por '.' e retira o cifrão
        price = book_html.find("span", {"class": "a-price"})\
            .find("span", {"class": "a-offscreen"}).text.strip()\
            .replace("R$\xa0", "").replace(",", ".")
        price = float(price)
    
    # Busca o atributo 'src' da tag 'img'
    image = book_html.find("div", {"class": "g-itemImage"}).find("img")["src"]

    # Busca o atributo 'href' da tag 'a' e concatena com a parte inicial da url da amazon
    link = "https://www.amazon.com.br" + \
        book_html.find("a", {"class": "a-link-normal"})["href"].strip()

    # Busca as informações do livro, onde o autor e o tipo do livro ficam na mesma string
    book_info = book_html.find("div", {"class": "g-span12when-narrow"})\
        .find("span", {"class": "a-size-base"}).text.strip()

    # Retira apenas a parte do tipo de livro, que começa no caractere '('
    book_type = book_info[book_info.find("(")+1:-1]

    # Retira apenas a parte do autor do livro, que termina no caractere '('
    author = book_info[3:book_info.find("(")-1]

    review = None
    # Checa se o livro possui avaliações
    if book_html.find("i", {"class": {"a-icon-star-small"}}):
        # Busca pelo texto da tag 'i' e retira a parte final, para obter apenas o valor da avaliação
        review = book_html.find("i", {"class": {"a-icon-star-small"}})\
            .text.strip().replace(" de 5 estrelas", "")
    
    price_dropped = None
    # Verifica se o preço do livro caiu
    if book_html.find("div", {"class": "itemPriceDrop"}):
        # Em caso positivo, busca pelo texto do elemento e retira a parte inicial, para obter apenas o valor
        price_dropped = book_html.find("div", {"class": "itemPriceDrop"})\
            .find("span", {"class": "a-text-bold"}).text.strip()\
            .replace("Preço caiu ", "").replace("Queda de preço em ", "")\
            .replace(",", ".")
        # O valor pode vir em porcentagem, ou o valor absoluto (R$)
        if '%' in price_dropped:
            # Caso seja a porcentagem, multiplicamos pelo preço do livro para obter o valor absoluto
            percentage_price_dropped = float(price_dropped.replace("%", "")) / 100
            price_original = price * (1 + percentage_price_dropped)
            price_dropped = round(price_original - price, 2)
        else:
            price_dropped = price_dropped.replace("R$ ", "").replace(",", ".")

    row = (
        title, price, image, link, author, book_type, review, price_dropped
    )

    return row

def check_next_page(html: soup) -> str:
    """
        Verifica se possui uma próxima página a ser carregada.
        Retorna uma string caso possua a página, ou None caso contrário.
    """

    # Busca pela tag que contém a url da proxima página
    next_page = html.find("script", {"data-a-state": '{"key":"scrollState"}'})

    # Transforma a string em um dicionario
    next_page_json = json.loads(next_page.text)
    
    next_page_url = None
    # Caso a chave 'lastEvaluatedKey' possua um valor, então tem proxima página
    if next_page_json["lastEvaluatedKey"] != "":
        # Concatena o valor da chave 'showMoreUrl' com a url da amazon, para formar a url da proxima pagina
        next_page_url = "https://www.amazon.com.br" + next_page_json["showMoreUrl"]

    return next_page_url