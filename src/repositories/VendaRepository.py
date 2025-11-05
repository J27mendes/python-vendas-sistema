from datetime import date, datetime
import sqlite3
from src.models.Venda import Venda
from src.utils.Database import obter_caminho_banco
from typing import List, Tuple

class VendaRepository:

    @staticmethod
    def criar_venda(venda: Venda):
        """Insere uma venda no banco de dados (ajusta a data para string antes de inserir) e retorna o ID gerado."""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Formata a data para string no formato YYYY-MM-DD para o SQLite
            data_str = venda.data.strftime('%Y-%m-%d')
            
            # Insere a venda no banco e obtém o id gerado automaticamente
            cursor.execute('''INSERT INTO Vendas (produto_id, quantidade, data, preco_unitario) 
                              VALUES (?, ?, ?, ?)''', 
                           (venda.produto_id, venda.quantidade, data_str, venda.preco_unitario))
            
            # Obtém o ID gerado automaticamente para a venda
            venda.id = cursor.lastrowid  # Atribui o ID gerado pelo banco à venda
            
            conn.commit()
            conn.close()
            print(f"Venda criada com sucesso! ID da venda: {venda.id}")
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
            
            # Agora, para cada venda, obtemos o preco_unitario
            vendas_obj = []
            for venda in vendas:
                produto_id = venda[1]
                preco_unitario = VendaRepository.obter_preco_produto(produto_id)
                # Cria a instância de Venda usando o preco_unitario obtido
                vendas_obj.append(Venda(venda[1], venda[2], venda[3], preco_unitario))
            
            return vendas_obj
        except sqlite3.Error as e:
            print(f"Erro ao obter vendas: {e}")
            return []
        
    @staticmethod
    def obter_preco_produto(produto_id: int) -> float:
        """Obtém o preço do produto pelo ID"""
        db_path = obter_caminho_banco()
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT preco FROM Produtos WHERE id = ?", (produto_id,))
        preco = cursor.fetchone()
        conn.close()
        return preco[0] if preco else 0.0
    
    @staticmethod
    def inserir_vendas(vendas: list):
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.executemany('''INSERT INTO Vendas (produto_id, quantidade, data, preco_unitario) VALUES (?, ?, ?)''', vendas)
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
        
    @staticmethod
    def obter_venda_por_id(venda_id: int) -> Venda or None: # type: ignore
        """Busca uma venda pelo ID no banco de dados e retorna um objeto Venda"""
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
        
            # Ajuste na consulta SQL para incluir o preco_unitario
            cursor.execute("""
                SELECT v.id, v.produto_id, v.quantidade, v.data, p.preco AS preco_unitario
                FROM Vendas v
                INNER JOIN Produtos p ON v.produto_id = p.id
                WHERE v.id = ?
            """, (venda_id,))
        
            venda_data = cursor.fetchone()
            conn.close()
        
            if venda_data:
                # Separando o id dos outros dados e criando a instância de Venda sem problemas
                venda_id, produto_id, quantidade, data, preco_unitario = venda_data
                return Venda(produto_id=produto_id, quantidade=quantidade, data=data, preco_unitario=preco_unitario, id=venda_id)
            else:
                return None  # Retorna None se não encontrar a venda
    
        except sqlite3.Error as e:
            print(f"Erro ao buscar venda: {e}")
        return None