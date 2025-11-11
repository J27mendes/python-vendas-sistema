from datetime import date, datetime
import sqlite3
from src.models.Venda import Venda
from src.repositories.BaseRepository import BaseRepository 
from typing import List, Tuple, Optional
class VendaRepository(BaseRepository):

    def __init__(self):
        # Chama o construtor da classe base, definindo a tabela como 'Vendas'
        super().__init__('Vendas')
        
    def criar_venda(self, venda: Venda):
        """Insere uma venda no banco de dados e retorna o ID gerado."""
        try:
            with self._conectar_db() as (conn, cursor):
                
                # Garante que a data está no formato de string YYYY-MM-DD
                data_str = venda.data.strftime('%Y-%m-%d')
                
                cursor.execute('''INSERT INTO Vendas (produto_id, quantidade, data, preco_unitario) 
                                 VALUES (?, ?, ?, ?)''', 
                               (venda.produto_id, venda.quantidade, data_str, venda.preco_unitario))
                
                venda.id = cursor.lastrowid
                conn.commit()
                print(f"Venda criada com sucesso! ID da venda: {venda.id}")
        except sqlite3.Error as e:
            print(f"Erro ao criar venda: {e}")

    def obter_vendas(self) -> List[Venda]:
        """Retorna todas as vendas registradas no banco."""
        try:
            with self._conectar_db() as (_, cursor):
                cursor.execute("SELECT id, produto_id, quantidade, data, preco_unitario FROM Vendas")
                vendas = cursor.fetchall()
            
            vendas_obj = []
            for v in vendas:
                vendas_obj.append(Venda(id=v[0], produto_id=v[1], quantidade=v[2], data=v[3], preco_unitario=v[4]))
            
            return vendas_obj
        except sqlite3.Error as e:
            print(f"Erro ao obter vendas: {e}")
            return []
        
    def _obter_preco_produto(self, produto_id: int) -> float:
        """Obtém o preço do produto pelo ID. (Método auxiliar de instância)"""
        try:
            with self._conectar_db() as (_, cursor):
                cursor.execute("SELECT preco FROM Produtos WHERE id = ?", (produto_id,))
                preco = cursor.fetchone()
                return preco[0] if preco else 0.0
        except sqlite3.Error as e:
             print(f"Erro ao obter preço do produto: {e}")
             return 0.0
    
    def inserir_vendas(self, vendas: list):
        """Insere várias vendas de uma vez. (Método de instância)"""
        try:
            with self._conectar_db() as (conn, cursor):
                cursor.executemany('''INSERT INTO Vendas (produto_id, quantidade, data, preco_unitario) 
                                     VALUES (?, ?, ?, ?)''', vendas)
                conn.commit()
                print("Vendas inseridas com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao inserir as vendas: {e}") 

    def obter_vendas_por_produto(self) -> List[Tuple[int, int, float]]:
        """Obtém a quantidade de vendas e o total somado de cada produto. (Método de instância)"""
        try:
            with self._conectar_db() as (_, cursor):
                # A consulta usa preco_unitario da tabela Vendas, se estiver preenchida corretamente.
                query = '''
                SELECT p.id, SUM(v.quantidade) AS quantidade_vendida, SUM(v.quantidade * v.preco_unitario) AS valor_total
                FROM Vendas v
                INNER JOIN Produtos p ON v.produto_id = p.id
                GROUP BY p.id
                '''
                cursor.execute(query)
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao calcular vendas por produto: {e}")
            return []
        
    def obter_venda_por_id(self, venda_id: int) -> Optional[Venda]:
        """Busca uma venda pelo ID no banco de dados e retorna um objeto Venda. (Método de instância)"""
        try:
            with self._conectar_db() as (_, cursor):
                cursor.execute("""
                    SELECT id, produto_id, quantidade, data, preco_unitario
                    FROM Vendas
                    WHERE id = ?
                """, (venda_id,))
                
                venda_data = cursor.fetchone()
            
            if venda_data:
                venda_id, produto_id, quantidade, data, preco_unitario = venda_data
                return Venda(produto_id=produto_id, quantidade=quantidade, data=data, preco_unitario=preco_unitario, id=venda_id)
            else:
                return None
        except sqlite3.Error as e:
            print(f"Erro ao buscar venda por ID: {e}")
            return None
    
    def atualizar_venda(self, venda: Venda):
        """Atualiza os dados de uma venda no banco de dados. (Método de instância)"""
        try:
            with self._conectar_db() as (conn, cursor):
                if isinstance(venda.data, (datetime, date)):
                    data_str = venda.data.strftime('%Y-%m-%d')
                elif isinstance(venda.data, str):
                    data_str = venda.data 
                else:
                    raise ValueError("Data fornecida não está no formato correto")
                
                cursor.execute('''
                    UPDATE Vendas 
                    SET produto_id = ?, quantidade = ?, data = ?, preco_unitario = ?
                    WHERE id = ?
                ''', (venda.produto_id, venda.quantidade, data_str, venda.preco_unitario, venda.id))

                conn.commit()
                print(f"Venda ID {venda.id} atualizada com sucesso!")

        except sqlite3.Error as e:
            print(f"Erro ao atualizar venda: {e}")
        except Exception as e:
            print(f"Erro inesperado ao atualizar venda: {e}")
