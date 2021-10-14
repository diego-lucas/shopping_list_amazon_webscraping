# Webscraping da Lista de compras da Amazon
O projeto faz um webscraping de uma lista de compras da Amazon. Para funcionar, a lista precisa estar pública.
Foi desenvolvido utilizando apenas livros na lista.

## Tecnologias
Foi utilizado Python 3 para o desenvolvimento do projeto, utilizando as bibliotecas requests, BeautifulSoup, json e psycopg2.

## Desenvolvimento
É feito uma requisição à página da Amazon, e então faz a leitura dos itens carregados. Os itens são carregados assíncronamente na página, de 10 em 10.
Por isso, é necessário buscar um link temporário que carrega o próximo lote de itens. E por fim, os dados são enviados para um banco de dados PostgreSQL.