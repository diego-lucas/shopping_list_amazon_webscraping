import psycopg2
from psycopg2.extras import execute_values


def connect_database(database):
    """
        Faz a conexão com o banco de dados utilizando a lib psycopg2.
        Retorna a conexão e o cursor.
    """

    # Cria a conexão com o banco de dados
    connection = psycopg2.connect(host='localhost', port=5432, database=database, user='postgres', password='123')
    # Cria um cursor sobre a conexão
    cursor = connection.cursor()

    return connection, cursor

def insert_database(database, table, data, columns):

    """
        Com uma conexão ao banco de dados Postgres, trunca a tabela informada e insere os dados.
    """

    # Criar a conexão e o cursor com o banco
    conn, cursor = connect_database(database)

    # Cria o header das colunas para passar na query
    header = ','.join(columns)

    print("Truncando tabela.")
    # Limpa os dados existentes na tabela
    cursor.execute("TRUNCATE TABLE " + table)

    print(f"Inserindo {len(data)} linhas.")
    # Cria a query de inserção
    query = f"INSERT INTO {table} ({header}) VALUES %s"

    # Utiliza a função do psycopg para inserir os dados
    execute_values(cursor, query, data)

    # Commita as alterações
    conn.commit()
    
    print("Dados inseridos.")
