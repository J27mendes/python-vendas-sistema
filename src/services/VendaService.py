import re
from typing import List, Tuple
from datetime import datetime
from src.models.Venda import Venda
from src.repositories.VendaRepository import VendaRepository
class VendaService:

    @staticmethod
    def registrar_venda(produto_id, quantidade, preco_unitario, data):
        """Registra a venda no banco de dados."""
        try:
            # Criação do objeto Venda, incluindo o preco_unitario
            venda = Venda(produto_id=produto_id, quantidade=quantidade, preco_unitario=preco_unitario, data=data)
            VendaRepository.criar_venda(venda)
            return True
        except Exception as e:
            print(f"Erro ao registrar a venda: {e}")
            return False

    @staticmethod
    def registrar_vendas(vendas: List[Tuple[int, int, str]]):
        """Chama o repositório para registrar várias vendas no banco"""
        VendaRepository.inserir_vendas(vendas)

    @staticmethod
    def atualizar_venda(venda_id: int, novo_produto_id: int, nova_quantidade: int, nova_data: str) -> bool:
        """Atualiza uma venda existente no banco de dados."""
        try:
            # Verifica se a venda existe antes de tentar atualizar
            venda = VendaRepository.obter_venda_por_id(venda_id)
            if not venda:
                print("Venda não encontrada!")
                return False
            
            # Atualiza os dados da venda com os novos valores
            venda.produto_id = novo_produto_id if novo_produto_id else venda.produto_id
            venda.quantidade = nova_quantidade if nova_quantidade else venda.quantidade

            # Converte nova_data para o tipo datetime.date, se necessário
            if nova_data:
                nova_data = nova_data.strip()
                print(f"Data fornecida para conversão: '{nova_data}'")
                try:
                    # Converte nova_data para datetime.date
                    venda.data = datetime.strptime(nova_data, '%Y-%m-%d').date()
                    print("Data convertida no service:", venda.data)
                except ValueError:
                    print("❗ A data fornecida não está no formato correto (AAAA-MM-DD).")
                    return False
            
            # Chama o repositório para atualizar a venda
            VendaRepository.atualizar_venda(venda)
            return True
        except Exception as e:
            print(f"Ocorreu um erro ao atualizar a venda: {e}")
            return False
        
    @staticmethod
    def obter_vendas():
        """Retorna todas as vendas registradas no banco de dados"""
        try:
            vendas = VendaRepository.obter_vendas()  
            return vendas
        except Exception as e:
            print(f"Erro ao obter vendas no service: {e}")
            return []
        
    @staticmethod
    def deletar_venda(venda_id: int) -> bool:
        """Deleta uma venda existente no banco de dados."""
        try:
            # Verifica se a venda existe
            venda = VendaRepository.obter_venda_por_id(venda_id)
            if not venda:
                print("Venda não encontrada!")
                return False
            
            # Chama o repositório para deletar a venda
            VendaRepository.deletar_venda(venda_id)
            print(f"Venda ID {venda_id} deletada com sucesso!")
            return True
        except Exception as e:
            print(f"Ocorreu um erro ao deletar a venda: {e}")
            return False