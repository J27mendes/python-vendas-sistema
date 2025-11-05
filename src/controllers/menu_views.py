import sys
import os
import re
from typing import List, Tuple

from utils.Database import criar_banco_de_dados

# Adiciona o diretório 'src' ao sys.path para garantir que o Python consiga localizar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from repositories.ProdutoRepository import ProdutoRepository
from src.repositories.ProdutoRepository import ProdutoRepository
from repositories.VendaRepository import VendaRepository
from src.services.ProdutoService import ProdutoService
from src.services.VendaService import VendaService
from src.models.Produto import Produto
from src.models.Venda import Venda

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

