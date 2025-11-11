from typing import Optional
from .BaseModel import BaseModel 
class Produto(BaseModel):
    def __init__(self, id: Optional[int], nome: str, categoria: str, preco: float):
        
        super().__init__(id) 
        
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
    
    def __repr__(self):
        
        return f"Produto(id={self.id}, nome={self.nome}, categoria={self.categoria}, preco={self.preco})"