import re
from typing import List, Tuple
from datetime import datetime
from src.repositories.VendaRepository import VendaRepository
class VendaService:
    @staticmethod
    def registrar_venda() -> List[Tuple[int, int, str]]:
        """Função para solicitar a entrada de dados para vendas"""
        vendas = []
        while True:
            try:
                # 1. ENTRADA E VALIDAÇÃO DE ID
                produto_id = int(input("Digite o ID do produto (1-6) ou 0 para finalizar: "))
                
                if produto_id == 0:
                    break  

                if produto_id not in range(1, 7): 
                    print("Produto ID inválido. Digite um valor entre 1 e 6.")
                    continue

                # 2. ENTRADA E VALIDAÇÃO DE QUANTIDADE
                quantidade = int(input(f"Digite a quantidade de {produto_id}: "))
                if quantidade <= 0:
                    print("Quantidade deve ser um número positivo maior que zero.")
                    continue

                # 3. ENTRADA E VALIDAÇÃO DE DATA
                data = input("Digite a data da venda (AAAA-MM-DD): ")
                
                if not re.match(r'\d{4}-\d{2}-\d{2}', data):
                    print("Formato de data inválido. Use o formato AAAA-MM-DD.")
                    continue

                try:
                    datetime.strptime(data, '%Y-%m-%d')
                except ValueError:
                    print("Data inválida. O mês ou o dia inserido não existe (ex: mês 13 ou dia 30 em fevereiro).")
                    continue
                
                vendas.append((produto_id, quantidade, data))
                
            except ValueError:
                # Captura erros se o usuário digitar texto onde é esperado um número (ID ou Quantidade)
                print("Entrada inválida! Por favor, insira números válidos.")
            except Exception as e:
                # Captura quaisquer outros erros inesperados
                print(f"Ocorreu um erro inesperado: {e}")
                
        return vendas

    @staticmethod
    def registrar_vendas(vendas: List[Tuple[int, int, str]]):
        """Chama o repositório para registrar várias vendas no banco"""
        VendaRepository.inserir_vendas(vendas)