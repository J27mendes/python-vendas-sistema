import sys
import os
from typing import List, Tuple, TYPE_CHECKING
from src.models.Produto import Produto

if TYPE_CHECKING:
    from src.repositories.ProdutoRepository import ProdutoRepository
    from src.repositories.VendaRepository import VendaRepository

class ProdutoService:
    """
    Camada de Serviço (Lógica de Negócios) para a entidade Produto.
    Os métodos recebem a instância do repositório como dependência.

    """

    @staticmethod
    def cadastrar_produto(nome: str, categoria: str, preco: float, produto_repo: 'ProdutoRepository'):
        """Cadastra um novo produto, usando o repositório injetado."""
        produto = Produto(None, nome, categoria, preco)  # ID será autoincrementado
        try:
            produto_repo.criar_produto(produto) 
        except Exception as e:
            print(f"Erro ao cadastrar produto no Service: {e}")

    @staticmethod
    def carregar_dados_simulados(produto_repo: 'ProdutoRepository'):
        """Carregar dados simulados, usando o repositório injetado."""
        try:
            produto_repo.carregar_dados_simulados()
        except Exception as e:
            print(f"Erro ao carregar dados simulados no Service: {e}")

    @staticmethod
    def listar_produtos_e_ids(produto_repo: 'ProdutoRepository'):
        """Obtém todos os produtos do Repository e os imprime formatados."""
        
        produtos = produto_repo.obter_produtos()
            
        print("\n" + "="*50)
        print("PRODUTOS ATUAIS CADASTRADOS NO BANCO")
        
        if not produtos:
            print("Nenhum produto encontrado.")
            return

        # 2. Imprime o cabeçalho
        print(f"{'ID':<5} {'NOME':<25} {'CATEGORIA':<20} {'PREÇO':<10}")
        print("-" * 50)
            
        for p in produtos:
            try:
                print(f"{p.id:<5} {p.nome:<25} {p.categoria:<20} R${p.preco:.2f}")
            except AttributeError:
                print("Erro ao listar produto. Verifique a estrutura da classe Produto.")
                    
        print("-"*50)

    @staticmethod
    def buscar_produto_por_id(produto_id: int, produto_repo: 'ProdutoRepository') -> Produto or None: # type: ignore
        """
        Busca um produto específico no repositório.
        Retorna o objeto Produto ou None.

        """
        produto = produto_repo.obter_produto_por_id(produto_id) 
        
        if produto is None:
            print(f"Produto com ID {produto_id} não encontrado.")
        
        return produto
    
    @staticmethod
    def listar_produtos_vendidos(produto_repo: 'ProdutoRepository', venda_repo: 'VendaRepository'):
        """Exibe a quantidade vendida e o valor total de cada produto (requer ambos repositórios)."""
        
        try:
            vendas_agregadas = venda_repo.obter_vendas_por_produto()
            
            if not vendas_agregadas:
                print("Nenhuma venda registrada.")
                return
            
            print("\n" + "="*50)
            print("🛒 QUANTIDADE E VALOR DE VENDAS POR PRODUTO")
            print("="*50)
            print(f"{'ID':<5} {'NOME':<25} {'QUANTIDADE VENDIDA':<20} {'VALOR TOTAL':<15}")
            print("-" * 50)

            for venda in vendas_agregadas:
                # venda é uma tupla: (produto_id, quantidade_vendida, valor_total)
                produto_id, quantidade_vendida, valor_total = venda
                
                # Busca o produto para obter o nome, usando o produto_repo injetado
                produto = produto_repo.obter_produto_por_id(produto_id) 
                
                nome_produto = produto.nome if produto else "Produto Desconhecido"
                
                print(f"{produto_id:<5} {nome_produto:<25} {quantidade_vendida:<20} R${valor_total:.2f}")
            
            print("-" * 50)
        
        except Exception as e:
            print(f"Ocorreu um erro ao listar produtos vendidos no Service: {e}")


    @staticmethod
    def buscar_produtos(produto_repo: 'ProdutoRepository'):
        """Busca todos os produtos no banco de dados e retorna como uma lista."""
        try:
            produtos = produto_repo.obter_produtos() 
            return produtos
        except Exception as e:
            print(f"Ocorreu um erro ao listar os produtos: {e}")
            return []
            
    @staticmethod
    def atualizar_produto(produto_id: int, nome: str, categoria: str, preco: float, produto_repo: 'ProdutoRepository'):
        """Atualiza as informações de um produto no banco de dados."""
        try:
            # 1. Verifica se o produto existe
            produto = produto_repo.obter_produto_por_id(produto_id)
            if not produto:
                print("Produto não encontrado!")
                return False
            
            # 2. Atualiza as informações do produto
            produto.nome = nome
            produto.categoria = categoria
            produto.preco = preco

            produto_repo.atualizar_produto(produto)
            print(f"Produto {produto_id} atualizado com sucesso!")
            return True
        
        except Exception as e:
            print(f"Ocorreu um erro ao atualizar o produto no Service: {e}")
            return False
