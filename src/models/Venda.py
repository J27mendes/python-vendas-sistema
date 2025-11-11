from typing import Optional
from datetime import datetime, date
import sqlite3

from .BaseModel import BaseModel 
from src.utils.Database import obter_caminho_banco

# Venda herda de BaseModel
class Venda(BaseModel):
    def __init__(self, produto_id: int, quantidade: int, data: str, preco_unitario: float, id: Optional[int] = None):
       
        super().__init__(id) 
        
        self.produto_id = produto_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario    
        self.data: Optional[date] = None  # Garante que self.data seja inicializado como Optional[date]
        
        if isinstance(data, str):
            self.data = self.converter_data(data)
        elif isinstance(data, (date, datetime)): # Usando date do import
            self.data = data.date() if isinstance(data, datetime) else data
        else:
            self.data = None
    
    def __repr__(self):
        return f"Venda(id={self.id}, produto_id={self.produto_id}, quantidade={self.quantidade}, data={self.data}, preço unitário={self.preco_unitario})"
    
    @staticmethod
    def converter_data(data: str) -> Optional[date]: # Usando date
        """Converte a string de data para o tipo datetime.date"""
        try:
            return datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            print(f"Erro ao converter data: {data}. O formato correto é 'YYYY-MM-DD'.")
            return None

    @classmethod
    def from_tuple(cls, venda_data: tuple):
        """Cria uma instância de Venda a partir de dados do banco"""
        
        return cls(venda_data[1], venda_data[2], venda_data[3], venda_data[4], venda_data[0])

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
    
    @property
    def total(self):
        """Calcula o total da venda (quantidade * preço)"""
        return self.quantidade * self.preco_unitario