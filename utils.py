import re
import requests


def make_request(shopping_list_url: str) -> bytes:
    """
        Checa se a url informada está adequada, e então faz a requisição para a página.
        Retorna o conteúdo da requisição, que é o HTML da página.
    """

    # Valida a URL informada, se não seguir o padrão é retornado um erro
    if not validate_amazon_url(shopping_list_url):
        raise NotImplementedError(
            "A URL informada não é de uma lista de compras da Amazon."
        )

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
    }

    # Faz a requisição GET a url
    response = requests.get(shopping_list_url, headers=headers)

    # Busca o conteúdo da requisição, que é o html da página
    html = response.content

    return html

def validate_amazon_url(url: str) -> bool:
    """
        Valida se a url informada faz parte do domínio da Amazon e segue o padrão correto.
        Retorna um booleano.
    """

    # Checa se a url é uma string
    if isinstance(url, str):

        # Define o padrão da url com regex
        url_pattern = re.compile("(http(s)?://)?(www.)?amazon.com.br/hz/wishlist")

        # Checa se o url informada segue o padrão definido
        match = url_pattern.match(url)

        return bool(match)
    
    return False

