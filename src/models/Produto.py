class Produto:
    def __init__(self, id: int, nome: str, categoria: str, preco: float):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.preco = preco
    
    def __repr__(self):
        return f"Produto(id={self.id}, nome={self.nome}, categoria={self.categoria}, preco={self.preco})"