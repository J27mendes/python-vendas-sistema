import sys
import os
import re
from typing import List, Tuple
from datetime import datetime

# Adiciona o diretório 'src' ao sys.path para garantir que o Python consiga localizar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from repositories.ProdutoRepository import ProdutoRepository
from repositories.VendaRepository import VendaRepository
from src.services.ProdutoService import ProdutoService
from src.services.VendaService import VendaService

def buscar_produtos_interativo():
    """Permite ao usuário visualizar todos os produtos cadastrados no banco."""
    
    print("\n" + "="*50)
    print("LISTA DE PRODUTOS")
    print("="*50)
    
    try:
        # 1. Chama o serviço para buscar todos os produtos
        produtos = ProdutoService.buscar_produtos()  # Usa o serviço ProdutoService para buscar os produtos
        
        # 2. Exibe os produtos encontrados
        if produtos:
            for produto in produtos:
                print(f"ID: {produto.id} | Nome: {produto.nome} | Categoria: {produto.categoria} | Preço: R$ {produto.preco:.2f}")
        else:
            print("Nenhum produto cadastrado.")
    
    except Exception as e:
        print(f"Ocorreu um erro ao listar os produtos: {e}")

def atualizar_produto():
    """Permite ao usuário atualizar as informações de um produto existente."""
    
    print("\n" + "="*50)
    print("ATUALIZAR PRODUTO")
    print("="*50)

    try:
        # 1. Solicita o ID do produto que deseja atualizar
        produto_id = int(input("Digite o ID do produto que deseja atualizar: "))
        
        # 2. Verifica se o produto existe (chama o serviço)
        produto = ProdutoRepository.obter_produto_por_id(produto_id)
        
        if not produto:
            print("Produto não encontrado!")
            return
        
        # 3. Exibe as informações atuais do produto
        print(f"\n--- Informações atuais do produto ---")
        print(f"ID: {produto.id}")
        print(f"Nome: {produto.nome}")
        print(f"Categoria: {produto.categoria}")
        print(f"Preço: R$ {produto.preco:.2f}")
        print("-------------------------------------\n")
        
        # 4. Solicita as novas informações do produto
        nome = input(f"Novo nome (deixe em branco para manter '{produto.nome}'): ")
        categoria = input(f"Nova categoria (deixe em branco para manter '{produto.categoria}'): ")
        preco = input(f"Novo preço (deixe em branco para manter R$ {produto.preco:.2f}): ")

        # 5. Atualiza as informações somente se o usuário fornecer um valor
        nome = nome if nome else produto.nome
        categoria = categoria if categoria else produto.categoria
        preco = float(preco) if preco else produto.preco
        
        # 6. Chama o serviço para atualizar o produto
        if ProdutoService.atualizar_produto(produto_id, nome, categoria, preco):
            print("\nProduto atualizado com sucesso!")
        else:
            print("Não foi possível atualizar o produto.")

    except ValueError:
        print("❗ Entrada inválida. Por favor, insira os dados corretamente.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def ver_vendas_interativo():
    """Exibe todas as vendas"""
    try:
        vendas = VendaService.obter_vendas()  # Chama o service para obter as vendas
        
        if vendas:
            print("\n" + "="*50)
            print("LISTA DE VENDAS")
            print("="*50)
            for venda in vendas:
                # Garanta que 'venda.total' é um número e exiba corretamente
                print(f"Produto ID: {venda.produto_id} | Quantidade: {venda.quantidade} | Data: {venda.data} | Total: R$ {float(venda.total):.2f}")
        else:
            print("Nenhuma venda registrada.")
    except Exception as e:
        print(f"Ocorreu um erro ao exibir as vendas: {e}")

def registrar_venda_interativo():
    """Função para solicitar a entrada de dados para vendas e registrar no banco de dados."""
    
    while True:
        try:
            # 1. ENTRADA E VALIDAÇÃO DE ID
            produto_id = int(input("Digite o ID do produto (1-6) ou 0 para finalizar: "))
            
            if produto_id == 0:
                print("Finalizando o registro de vendas.")
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
                # Verifica se a data inserida é válida
                datetime.strptime(data, '%Y-%m-%d')
            except ValueError:
                print("Data inválida. O mês ou o dia inserido não existe (ex: mês 13 ou dia 30 em fevereiro).")
                continue

            # 4. Buscar o preço do produto para calcular o preço unitário
            produto = ProdutoRepository.obter_produto_por_id(produto_id)  # Certifique-se que o método está correto
            if produto:
                preco_unitario = produto.preco  # Obtém o preço do produto
            else:
                print(f"Produto ID {produto_id} não encontrado.")
                continue

            # 5. Registro da venda no banco de dados
            if VendaService.registrar_venda(produto_id, quantidade, preco_unitario, data):
                print(f"Venda de {quantidade} unidades do produto ID {produto_id} registrada com sucesso!")
            else:
                print(f"Não foi possível registrar a venda para o produto ID {produto_id}.")

        except ValueError:
            # Captura erros se o usuário digitar texto onde é esperado um número (ID ou Quantidade)
            print("Entrada inválida! Por favor, insira números válidos.")
        except Exception as e:
            # Captura quaisquer outros erros inesperados
            print(f"Ocorreu um erro inesperado: {e}")

def atualizar_venda():
    """Permite ao usuário atualizar os dados de uma venda existente."""
    
    print("\n" + "="*50)
    print("ATUALIZAR VENDA")
    print("="*50)

    try:
        # 1. Solicita o ID da venda a ser atualizada
        venda_id = int(input("Digite o ID da venda que deseja atualizar: "))
        
        # 2. Verifica se a venda existe
        venda = VendaRepository.obter_venda_por_id(venda_id)
        
        if not venda:
            print("Venda não encontrada!")
            return
        
        # 3. Exibe as informações atuais da venda
        print(f"\n--- Informações atuais da venda ---")
        print(f"ID Venda: {venda.id}")
        print(f"Produto ID: {venda.produto_id}")
        print(f"Quantidade: {venda.quantidade}")
        print(f"Data: {venda.data}")
        print(f"Total: R$ {venda.total:.2f}")
        print("-------------------------------------\n")
        
        # 4. Solicita as novas informações para atualizar
        novo_produto_id = input(f"Novo Produto ID (deixe em branco para manter {venda.produto_id}): ")
        nova_quantidade = input(f"Nova Quantidade (deixe em branco para manter {venda.quantidade}): ")
        nova_data = input(f"Nova Data (deixe em branco para manter {venda.data}): ")

        # 5. Atualiza as informações fornecidas
        novo_produto_id = int(novo_produto_id) if novo_produto_id else venda.produto_id
        nova_quantidade = int(nova_quantidade) if nova_quantidade else venda.quantidade
        nova_data = nova_data if nova_data else venda.data

        # Atualiza a venda no banco de dados
        venda.produto_id = novo_produto_id
        venda.quantidade = nova_quantidade
        venda.data = nova_data
        
        VendaRepository.atualizar_venda(venda)
        print(f"\nVenda atualizada com sucesso!")
    
    except ValueError:
        print("❗ Entrada inválida. Por favor, insira os dados corretamente.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def deletar_venda():
    """Permite ao usuário deletar uma venda pelo ID."""
    
    print("\n" + "="*50)
    print("DELETAR VENDA")
    print("="*50)

    try:
        # 1. Solicita o ID da venda a ser deletada
        venda_id = int(input("Digite o ID da venda que deseja deletar: "))
        
        # 2. Chama o serviço para deletar a venda
        if VendaService.deletar_venda(venda_id):
            print(f"\nVenda ID {venda_id} deletada com sucesso!")
        else:
            print("Não foi possível deletar a venda.")
    
    except ValueError:
        print("❗ Entrada inválida. Por favor, insira um número para o ID da venda.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
