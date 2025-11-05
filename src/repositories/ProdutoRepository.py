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
        
    @staticmethod
    def produtos_mais_menos_vendidos() -> List[Tuple[str, int]]:
        """Obtém os produtos mais e menos vendidos"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            query = '''
            SELECT p.nome, SUM(v.quantidade) AS total_vendido
            FROM Vendas v
            INNER JOIN Produtos p ON v.produto_id = p.id
            GROUP BY p.id
            ORDER BY total_vendido DESC
            '''
            
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"Erro ao calcular os produtos mais vendidos: {e}")
            return []
        
    @staticmethod
    def vendas_por_categoria() -> List[Tuple[str, float]]:
        """Calcula as vendas totais por categoria"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            query = '''
            SELECT p.categoria, SUM(v.quantidade * p.preco) AS total_vendas
            FROM Vendas v
            INNER JOIN Produtos p ON v.produto_id = p.id
            GROUP BY p.categoria
            ORDER BY total_vendas DESC
            '''
            
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"Erro ao calcular vendas por categoria: {e}")
            return []    

    @staticmethod
    def obter_produto_por_id(produto_id: int) -> Produto or None: # type: ignore
        """
        Busca um único produto pelo seu ID usando a cláusula WHERE.
        Retorna um objeto Produto ou None se não for encontrado.
        """
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Consulta SQL com WHERE para filtrar pelo ID
            # '?' para consulta parametrizada (essencial para segurança)
            query = "SELECT id, nome, categoria, preco FROM Produtos WHERE id = ?"
            
            cursor.execute(query, (produto_id,)) # Passa a tupla com o ID
            produto_data = cursor.fetchone()
            conn.close()

            if produto_data:
                return Produto(*produto_data)
            else:
                return None
            
        except sqlite3.Error as e:
            print(f"Erro ao buscar produto por ID: {e}")
            return None
        
    @staticmethod
    def atualizar_produto(produto: Produto):
        """Atualiza um produto existente no banco de dados."""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            query = '''UPDATE Produtos
                       SET nome = ?, categoria = ?, preco = ?
                       WHERE id = ?'''
            cursor.execute(query, (produto.nome, produto.categoria, produto.preco, produto.id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            print(f"Erro ao atualizar produto: {e}")