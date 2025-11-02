from typing import Optional
import datetime
class Venda:
    def __init__(self, id: int, produto_id: int, quantidade: int, data):
        self.id = id
        self.produto_id = produto_id
        self.quantidade = quantidade
        
        # Converte se for string
        if isinstance(data, str):
            self.data = self.converter_data(data)
        elif isinstance(data, (datetime.date, datetime.datetime)):
            self.data = data.date() if isinstance(data, datetime.datetime) else data
        else:
            self.data = None
    
    def __repr__(self):
        return f"Venda(id={self.id}, produto_id={self.produto_id}, quantidade={self.quantidade}, data={self.data})"
    
    @staticmethod
    def converter_data(data: str) -> Optional[datetime.date]:
        """Converte a string de data para o tipo datetime.date"""
        try:
            return datetime.datetime.strptime(data, '%Y-%m-%d').date()
        except ValueError:
            print(f"Erro ao converter data: {data}. O formato correto é 'YYYY-MM-DD'.")
            return None

    @classmethod
    def from_tuple(cls, venda_data: tuple):
        """Cria uma instância de Venda a partir da tupla"""
        # Se for do banco (4 elementos), o primeiro é o ID
        if len(venda_data) == 4:
            id, produto_id, quantidade, data = venda_data
            return cls(id, produto_id, quantidade, data)
        # o ID é desnecessário aqui, se for da lista do service (3 elementos), 
        elif len(venda_data) == 3:
            produto_id, quantidade, data = venda_data
            return cls(None, produto_id, quantidade, data) # Passa None para o ID
        
        raise ValueError("Tupla de venda com número incorreto de elementos.")