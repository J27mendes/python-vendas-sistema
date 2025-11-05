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

