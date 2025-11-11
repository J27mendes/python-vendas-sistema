import re
from typing import List, Tuple, TYPE_CHECKING
from datetime import datetime
from src.models.Venda import Venda

if TYPE_CHECKING:
    from src.repositories.VendaRepository import VendaRepository
    from src.repositories.ProdutoRepository import ProdutoRepository
class VendaService:

    @staticmethod
    def registrar_venda(produto_id: int, quantidade: int, preco_unitario: float, data: str, venda_repo: 'VendaRepository') -> bool:
        """
        Registra a venda no banco de dados, recebendo o repositório como argumento.
        """
        try:
            nova_venda = Venda(produto_id=produto_id, quantidade=quantidade, preco_unitario=preco_unitario, data=data)
            
            venda_repo.criar_venda(nova_venda) 
            return True
        except Exception as e:
            print(f"Erro ao registrar a venda no Service: {e}")
            return False

    @staticmethod
    def atualizar_venda(venda_id: int, novo_produto_id: int, nova_quantidade: int, nova_data: str, venda_repo: 'VendaRepository') -> bool:
        """
        Atualiza uma venda existente no banco de dados, recebendo o repositório como argumento.
        """
        try:
            venda = venda_repo.obter_venda_por_id(venda_id)
            if not venda:
                print("Venda não encontrada!")
                return False

            venda.produto_id = novo_produto_id
            venda.quantidade = nova_quantidade
            
            # Atualiza a data com validação
            if nova_data:
                nova_data = nova_data.strip()
                try:
                    datetime.strptime(nova_data, '%Y-%m-%d')
                    venda.data = nova_data
                except ValueError:
                    print("❗ A data fornecida não está no formato correto (AAAA-MM-DD).")
                    return False
            
            venda_repo.atualizar_venda(venda)
            return True
        except Exception as e:
            print(f"Ocorreu um erro ao atualizar a venda no Service: {e}")
            return False
        
    @staticmethod
    def obter_vendas(venda_repo: 'VendaRepository') -> List[Venda]:
        """
        Retorna todas as vendas registradas no banco de dados, recebendo o repositório.
        """
        try:
            return venda_repo.obter_vendas()
        except Exception as e:
            print(f"Erro ao obter vendas no service: {e}")
            return []
        
    @staticmethod
    def deletar_venda(venda_id: int, venda_repo: 'VendaRepository') -> bool:
        """
        Deleta uma venda existente no banco de dados, recebendo o repositório.
        """
        try:
            venda = venda_repo.obter_venda_por_id(venda_id)
            if not venda:
                print("Venda não encontrada para exclusão!")
                return False
            
            venda_repo.deletar_generico(venda_id)
            return True
        except Exception as e:
            print(f"Ocorreu um erro ao deletar a venda no Service: {e}")
            return False

    @staticmethod
    def registrar_vendas(vendas: List[Venda], venda_repo: 'VendaRepository'):
        """Chama o repositório para registrar várias vendas no banco (método auxiliar)."""
        for venda in vendas:
            venda_repo.inserir_vendas(venda)