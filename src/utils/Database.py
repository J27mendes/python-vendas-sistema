import sqlite3
import os

def obter_caminho_banco():
   # Caminho absoluto para o banco de dados na pasta 'data'
   projeto_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório onde o script está localizado
   caminho_banco = os.path.join(projeto_dir, '..', '..', 'data', 'vendas.db')  # Caminho para a pasta 'data' na raiz do projeto
    
   # Garante que o diretório 'data' exista
   caminho_data = os.path.dirname(caminho_banco)
   if not os.path.exists(caminho_data):
      os.makedirs(caminho_data)

   return caminho_banco

def criar_banco_de_dados():
   try:
      db_path = obter_caminho_banco()
      conn = sqlite3.connect(db_path)
      cursor = conn.cursor()
        
      # Criando a tabela Produtos
      cursor.execute('''CREATE TABLE IF NOT EXISTS Produtos (
         id INTEGER PRIMARY KEY,
         nome TEXT NOT NULL,
         categoria TEXT NOT NULL,
         preco REAL NOT NULL
      )''')
        
      # Criando a tabela Vendas
      cursor.execute('''CREATE TABLE IF NOT EXISTS Vendas (
         id INTEGER PRIMARY KEY,
         produto_id INTEGER,
         quantidade INTEGER,
         data DATE,
         FOREIGN KEY (produto_id) REFERENCES Produtos(id)
      )''')
        
      conn.commit()
      conn.close()
      print("Banco de dados e tabelas criados com sucesso!")
   except sqlite3.Error as e:
      print(f"Erro ao criar o banco de dados: {e}")