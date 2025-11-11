import sqlite3
from typing import List, Tuple, Optional
from src.repositories.BaseRepository import BaseRepository 
from src.models.Produto import Produto
class ProdutoRepository(BaseRepository):
    
    def __init__(self):
        super().__init__('Produtos')

    
    def criar_produto(self, produto: Produto):
        """Insere um produto no banco de dados"""
        try:
            with self._conectar_db() as (conn, cursor):
                cursor.execute('''INSERT INTO Produtos (nome, categoria, preco) VALUES (?, ?, ?)''',
                               (produto.nome, produto.categoria, produto.preco))
                produto.id = cursor.lastrowid
                conn.commit()
        except Exception as e:
            print(f"Erro ao criar produto: {e}")

    def obter_produtos(self) -> List[Produto]:
        """Retorna todos os produtos registrados no banco"""
        try:
            with self._conectar_db() as (conn, cursor):
                cursor.execute("SELECT id, nome, categoria, preco FROM Produtos")
                produtos = cursor.fetchall()
            # Retorna a lista de objetos do Produto
            return [Produto(id=p[0], nome=p[1], categoria=p[2], preco=p[3]) for p in produtos]
        except Exception as e:
            print(f"Erro ao obter produtos: {e}")
            return [] 
    
    def carregar_dados_simulados(self):
        """Função para carregar dados simulados"""
        try:
            with self._conectar_db() as (conn, cursor):
                # Verifica se já existem produtos cadastrados
                cursor.execute("SELECT COUNT(*) FROM Produtos")
                count = cursor.fetchone()[0]
                
                if count == 0:
                    produtos = [
                        ('Produto A', 'Categoria 1', 27.99),
                        ('Produto B', 'Categoria 2', 32.99),
                        ('Produto C', 'Categoria 1', 28.99),
                        ('Produto D', 'Categoria 2', 30.99),
                        ('Produto E', 'Categoria 3', 49.99),
                        ('Produto F', 'Categoria 4', 52.49)
                    ]
                    cursor.executemany('''INSERT INTO Produtos (nome, categoria, preco) VALUES (?, ?, ?)''', produtos)
                    conn.commit()
                    print("Dados simulados carregados com sucesso!")
                else:
                    print("Produtos já existem no banco de dados.")
        except Exception as e:
            print(f"Erro ao carregar os dados simulados: {e}")

    def total_vendas_por_produto(self) -> List[Tuple[str, float]]:
        """Calcula o total de vendas por produto"""
        try:
            with self._conectar_db() as (conn, cursor):
                query = '''
                SELECT p.nome, SUM(v.quantidade * v.preco_unitario) AS total_vendas
                FROM Vendas v
                INNER JOIN Produtos p ON v.produto_id = p.id
                GROUP BY p.id
                ORDER BY total_vendas DESC
                '''
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao calcular o total de vendas: {e}")
            return []
        
    def media_preco_produtos(self) -> float:
        """Calcula a média de preço dos produtos"""
        try:
            with self._conectar_db() as (_, cursor):
                query = '''SELECT AVG(preco) FROM Produtos'''
                cursor.execute(query)
                result = cursor.fetchone()[0]
                return 0.0 if result is None else result
        except Exception as e:
            print(f"Erro ao calcular a média de preços: {e}")
            return 0.0
        
    def produtos_mais_menos_vendidos(self) -> List[Tuple[str, int]]:
        """Obtém os produtos mais e menos vendidos"""
        try:
            with self._conectar_db() as (_, cursor):
                query = '''
                SELECT p.nome, SUM(v.quantidade) AS total_vendido
                FROM Vendas v
                INNER JOIN Produtos p ON v.produto_id = p.id
                GROUP BY p.id
                ORDER BY total_vendido DESC
                '''
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao calcular os produtos mais vendidos: {e}")
            return []
        
    def vendas_por_categoria(self) -> List[Tuple[str, float]]:
        """Calcula as vendas totais por categoria"""
        try:
            with self._conectar_db() as (_, cursor):
                query = '''
                SELECT p.categoria, SUM(v.quantidade * v.preco_unitario) AS total_vendas
                FROM Vendas v
                INNER JOIN Produtos p ON v.produto_id = p.id
                GROUP BY p.categoria
                ORDER BY total_vendas DESC
                '''
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao calcular vendas por categoria: {e}")
            return []     

    def obter_produto_por_id(self, produto_id: int) -> Optional[Produto]:
        """Busca um único produto pelo seu ID."""
        try:
            with self._conectar_db() as (_, cursor):
                query = "SELECT id, nome, categoria, preco FROM Produtos WHERE id = ?"
                cursor.execute(query, (produto_id,))
                produto_data = cursor.fetchone()

            if produto_data:
                return Produto(*produto_data)
            else:
                return None
        except Exception as e:
            print(f"Erro ao buscar produto por ID: {e}")
            return None
        
    def atualizar_produto(self, produto: Produto):
        """Atualiza um produto existente no banco de dados."""
        try:
            with self._conectar_db() as (conn, cursor):
                query = '''UPDATE Produtos
                           SET nome = ?, categoria = ?, preco = ?
                           WHERE id = ?'''
                cursor.execute(query, (produto.nome, produto.categoria, produto.preco, produto.id))
                conn.commit()
        except Exception as e:
            print(f"Erro ao atualizar produto: {e}")