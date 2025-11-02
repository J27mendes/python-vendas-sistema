from src.repositories.ProdutoRepository import ProdutoRepository
from src.utils.RelatorioUtils import salvar_relatorio_csv
from typing import List, Tuple
class RelatorioService:
        
    @staticmethod
    def total_vendas_por_produto() -> List[Tuple[str, float]]:
        """Total de vendas por produto (delegação para o Repository)"""
        return ProdutoRepository.total_vendas_por_produto()

    @staticmethod
    def media_preco_produtos() -> float:
        """Média de preço dos produtos (delegação para o Repository)"""
        return ProdutoRepository.media_preco_produtos()

    @staticmethod
    def produtos_mais_menos_vendidos() -> List[Tuple[str, int]]:
        """Obtém os produtos mais e menos vendidos (delegação para o Repository)"""
        return ProdutoRepository.produtos_mais_menos_vendidos()
    
    @staticmethod
    def vendas_por_categoria() -> List[Tuple[str, float]]:
        """Calcula as vendas totais por categoria (delegação para o Repository)"""
        return ProdutoRepository.vendas_por_categoria()
    
