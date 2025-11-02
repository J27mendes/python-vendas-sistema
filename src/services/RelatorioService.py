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
    
def imprimir_relatorios():
    # Relatório de Total de Vendas por Produto
    print("\n" + "="*40)
    print("Relatório de Total de Vendas por Produto:")

    total_vendas = RelatorioService.total_vendas_por_produto()  # Usando o serviço
    for produto, total in total_vendas:
        print(f"{produto}: R${total:.2f}")
    salvar_relatorio_csv(total_vendas, 'relatorio_total_vendas.csv', ['Produto', 'Total de Vendas'])
    
    # Relatório de Média de Preço dos Produtos
    print("\n" + "="*40)
    print("Média de Preço dos Produtos:")
    
    media = RelatorioService.media_preco_produtos()  # Usando o serviço
    print(f"R${media:.2f}")
    
    salvar_relatorio_csv([("Média Geral", media)], 'relatorio_media_preco.csv', ['Descrição', 'Média de Preço'])
    
    # Relatório de Produtos Mais Vendidos
    print("\n" + "="*40)
    print("Produtos Mais Vendidos (Top 5):")
    
    mais_vendidos = RelatorioService.produtos_mais_menos_vendidos()  # Usando o serviço
    for produto, total in mais_vendidos[:5]:  # Limitando aos top 5
        print(f"{produto}: {total} unidades")
    salvar_relatorio_csv(mais_vendidos[:5], 'relatorio_produtos_mais_vendidos.csv', ['Produto', 'Total Vendido'])
    
    # Relatório de Vendas por Categoria
    print("\n" + "="*40)
    print("Vendas por Categoria:")
    
