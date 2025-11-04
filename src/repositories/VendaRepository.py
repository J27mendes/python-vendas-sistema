import sqlite3
from src.models.Venda import Venda
from src.utils.Database import obter_caminho_banco
from typing import List, Tuple

class VendaRepository:

    @staticmethod
    def criar_venda(venda: Venda):
        """Insere uma venda no banco de dados (ajusta a data para string antes de inserir)"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Formata a data para string no formato YYYY-MM-DD para o SQLite
            data_str = venda.data.strftime('%Y-%m-%d')
            
            cursor.execute('''INSERT INTO Vendas (produto_id, quantidade, data) VALUES (?, ?, ?)''',
                           (venda.produto_id, venda.quantidade, data_str))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao criar venda: {e}")

    @staticmethod
    def obter_vendas():
        """Retorna todas as vendas registradas no banco"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id, produto_id, quantidade, data FROM Vendas")
            vendas = cursor.fetchall()
            conn.close()
            # Cria o objeto a partir da tupla do BD
            return [Venda.from_tuple(venda) for venda in vendas]
        except sqlite3.Error as e:
            print(f"Erro ao obter vendas: {e}")
            return []
    
    @staticmethod
    def inserir_vendas(vendas: list):
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.executemany('''INSERT INTO Vendas (produto_id, quantidade, data) VALUES (?, ?, ?)''', vendas)
            conn.commit()
            conn.close()
            print("Vendas inseridas com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao inserir as vendas: {e}") 

    @staticmethod
    def obter_vendas_por_produto() -> List[Tuple[int, int, float]]:
        """Obtém a quantidade de vendas e o total somado de cada produto"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Consulta as vendas agrupadas por produto, somando a quantidade e multiplicando pela quantidade do preço do produto
            query = '''
            SELECT p.id, SUM(v.quantidade) AS quantidade_vendida, SUM(v.quantidade * p.preco) AS valor_total
            FROM Vendas v
            INNER JOIN Produtos p ON v.produto_id = p.id
            GROUP BY p.id
            '''
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"Erro ao calcular vendas: {e}")
            return []