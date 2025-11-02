from src.repositories.ProdutoRepository import ProdutoRepository
from src.models.Produto import Produto

class ProdutoService:
   def cadastrar_produto(self, nome: str, categoria: str, preco: float):
      produto = Produto(None, nome, categoria, preco)  # ID será autoincrementado
      ProdutoRepository.criar_produto(produto)
    
   @staticmethod
   def carregar_dados_simulados():
      """Carregar dados simulados"""
      ProdutoRepository.carregar_dados_simulados()

 