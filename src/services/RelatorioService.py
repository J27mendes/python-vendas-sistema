from typing import List, Tuple, TYPE_CHECKING
from src.utils.RelatorioUtils import salvar_relatorio_csv

if TYPE_CHECKING:
    from src.repositories.ProdutoRepository import ProdutoRepository
    
class RelatorioService:
    """
    Camada de Serviço responsável por gerar relatórios estatísticos.
    Todos os métodos recebem a instância do ProdutoRepository como dependência.

    """
    @staticmethod
    def total_vendas_por_produto(produto_repo: 'ProdutoRepository') -> List[Tuple[str, float]]:
        """Total de vendas por produto (delegação para o Repository)"""
        return produto_repo.total_vendas_por_produto()

    @staticmethod
    def media_preco_produtos(produto_repo: 'ProdutoRepository') -> float:
        """Média de preço dos produtos (delegação para o Repository)"""
        return produto_repo.media_preco_produtos()

    @staticmethod
    def produtos_mais_menos_vendidos(produto_repo: 'ProdutoRepository') -> List[Tuple[str, int]]:
        """Obtém os produtos mais e menos vendidos (delegação para o Repository)"""
        return produto_repo.produtos_mais_menos_vendidos()
    
    @staticmethod
    def vendas_por_categoria(produto_repo: 'ProdutoRepository') -> List[Tuple[str, float]]:
        """Calcula as vendas totais por categoria (delegação para o Repository)"""
        return produto_repo.vendas_por_categoria()
