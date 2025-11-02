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

   @staticmethod
   def listar_produtos_e_ids():
      """Obtém todos os produtos do Repository e os imprime formatados."""
      produtos = ProdutoRepository.obter_produtos()
        
      print("\n" + "="*50)
      print("PRODUTOS ATUAIS CADASTRADOS NO BANCO (Verifique Duplicações)")
        
      if not produtos:
         print("Nenhum produto encontrado. Verifique se 'criar_banco_de_dados' e 'carregar_dados_simulados' rodaram.")
         return

      # Imprime o cabeçalho
      print(f"{'ID':<5} {'NOME':<25} {'CATEGORIA':<20} {'PREÇO':<10}")
      print("-" * 50)
        
      for p in produtos:
         try:
            print(f"{p.id:<5} {p.nome:<25} {p.categoria:<20} R${p.preco:.2f}")
         except AttributeError:
            print("Erro ao listar produto. Verifique se sua classe Produto tem os atributos 'id', 'nome', 'categoria' e 'preco'.")
                
      print("-"*50)

   @staticmethod
   def buscar_produto_por_id(produto_id: int) -> Produto or None: # type: ignore
        """
        Busca um produto específico no repositório.
        Retorna o objeto Produto ou None.
        """
        produto = ProdutoRepository.obter_produto_por_id(produto_id)
        
        if produto is None:
            print(f"Produto com ID {produto_id} não encontrado.")
        
        return produto