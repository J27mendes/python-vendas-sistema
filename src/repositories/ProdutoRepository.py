import sqlite3
from typing import List, Tuple
from src.models.Produto import Produto
from src.utils.Database import obter_caminho_banco

class ProdutoRepository:

    @staticmethod
    def criar_produto(produto: Produto):
        """Insere um produto no banco de dados"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO Produtos (nome, categoria, preco) VALUES (?, ?, ?)''',
                           (produto.nome, produto.categoria, produto.preco))
            produto.id = cursor.lastrowid
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao criar produto: {e}")

    @staticmethod
    def obter_produtos():
        """Retorna todos os produtos registrados no banco"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Produtos")
            produtos = cursor.fetchall()
            conn.close()
            return [Produto(*produto) for produto in produtos]
        except sqlite3.Error as e:
            print(f"Erro ao obter produtos: {e}")
            return [] 
    
    @staticmethod
    def carregar_dados_simulados():
        """Função para carregar dados simulados"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Inserir produtos simulados se não existirem
            produtos = [
                ('Produto A', 'Categoria 1', 27.99),
                ('Produto B', 'Categoria 2', 32.99),
                ('Produto C', 'Categoria 1', 28.99),
                ('Produto D', 'Categoria 2', 30.99),
                ('Produto E', 'Categoria 3', 49.99),
                ('Produto F', 'Categoria 4', 52.49)
            ]
            
            # Verifica se já existem produtos cadastrados, para não duplicar
            cursor.execute("SELECT COUNT(*) FROM Produtos")
            count = cursor.fetchone()[0]
            
            if count == 0:
                cursor.executemany('''INSERT INTO Produtos (nome, categoria, preco) VALUES (?, ?, ?)''', produtos)
                conn.commit()
                print("Dados simulados carregados com sucesso!")
            else:
                print("Produtos já existem no banco de dados.")
                
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao carregar os dados simulados: {e}")

    @staticmethod
    def total_vendas_por_produto() -> List[Tuple[str, float]]:
        """Calcula o total de vendas por produto"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            query = '''
            SELECT p.nome, SUM(v.quantidade * p.preco) AS total_vendas
            FROM Vendas v
            INNER JOIN Produtos p ON v.produto_id = p.id
            GROUP BY p.id
            ORDER BY total_vendas DESC
            '''
            
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"Erro ao calcular o total de vendas: {e}")
            return []
        
    @staticmethod
    def media_preco_produtos() -> float:
        """Calcula a média de preço dos produtos"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            query = '''SELECT AVG(preco) FROM Produtos'''
            
            cursor.execute(query)
            result = cursor.fetchone()[0]
            conn.close()

            return 0.0 if result is None else result
        except sqlite3.Error as e:
            print(f"Erro ao calcular a média de preços: {e}")
            return 0.0