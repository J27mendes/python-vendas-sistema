import sqlite3
from src.models.Venda import Venda
from src.utils.Database import obter_caminho_banco

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