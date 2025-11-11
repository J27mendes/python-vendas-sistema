import sys
import os
import re
from typing import List, Tuple, TYPE_CHECKING
from datetime import datetime

from src.services.ProdutoService import ProdutoService
from src.services.VendaService import VendaService
from src.services.RelatorioService import RelatorioService
from src.utils.RelatorioUtils import salvar_relatorio_csv

# --- Anotações de Tipo para Pylance ---
if TYPE_CHECKING:
    from src.repositories.ProdutoRepository import ProdutoRepository
    from src.repositories.VendaRepository import VendaRepository

def buscar_produtos_interativo(produto_repo: 'ProdutoRepository'):
    """Permite ao usuário visualizar todos os produtos cadastrados no banco, usando a instância do repositório."""
    
    print("\n" + "="*50)
    print("LISTA DE PRODUTOS")
    print("="*50)
    
    try:
        # Chama o serviço, repassando a instância do repositório
        produtos = ProdutoService.buscar_produtos(produto_repo) 
        
        if produtos:
            for produto in produtos:
                print(f"ID: {produto.id} | Nome: {produto.nome} | Categoria: {produto.categoria} | Preço: R$ {produto.preco:.2f}")
        else:
            print("Nenhum produto cadastrado.")
    
    except Exception as e:
        print(f"Ocorreu um erro ao listar os produtos: {e}")

def atualizar_produto(produto_repo: 'ProdutoRepository'):
    """Permite ao usuário atualizar as informações de um produto existente."""
    
    print("\n" + "="*50)
    print("ATUALIZAR PRODUTO")
    print("="*50)

    try:
        produto_id_input = input("Digite o ID do produto que deseja atualizar: ")
        if not produto_id_input.isdigit():
            print("ID inválido. Digite um número.")
            return

        produto_id = int(produto_id_input)
        
        produto = ProdutoService.buscar_produto_por_id(produto_id, produto_repo)
        
        if not produto:
            print("Produto não encontrado!")
            return
        
        print(f"\n--- Informações atuais do produto ---")
        print(f"ID: {produto.id}")
        print(f"Nome: {produto.nome}")
        print(f"Categoria: {produto.categoria}")
        print(f"Preço: R$ {produto.preco:.2f}")
        print("-------------------------------------\n")
        
        nome = input(f"Novo nome (deixe em branco para manter '{produto.nome}'): ")
        categoria = input(f"Nova categoria (deixe em branco para manter '{produto.categoria}'): ")
        preco = input(f"Novo preço (deixe em branco para manter R$ {produto.preco:.2f}): ")

        nome = nome if nome else produto.nome
        categoria = categoria if categoria else produto.categoria
        
        preco_final = produto.preco
        if preco:
            try:
                preco_final = float(preco)
            except ValueError:
                print("❗ Preço inválido. Mantendo o preço antigo.")
                return
        
        if ProdutoService.atualizar_produto(produto_id, nome, categoria, preco_final, produto_repo):
            print("\nProduto atualizado com sucesso!")
        else:
            print("Não foi possível atualizar o produto.")

    except ValueError:
        print("❗ Entrada inválida. Por favor, insira os dados corretamente.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def ver_vendas_interativo(venda_repo: 'VendaRepository'):
    """Exibe todas as vendas, usando a instância do repositório."""
    try:
        vendas = VendaService.obter_vendas(venda_repo)
        
        if vendas:
            print("\n" + "="*50)
            print("LISTA DE VENDAS")
            print("="*50)
            for venda in vendas:
                print(f"ID: {venda.id} | Produto ID: {venda.produto_id} | Quantidade: {venda.quantidade} | Data: {venda.data} | Total: R$ {float(venda.total):.2f}")
        else:
            print("Nenhuma venda registrada.")
    except Exception as e:
        print(f"Ocorreu um erro ao exibir as vendas: {e}")

def registrar_venda_interativo(venda_repo: 'VendaRepository', produto_repo: 'ProdutoRepository'):
    """Função para solicitar a entrada de dados para vendas e registrar no banco de dados."""
    
    print("\n" + "="*50)
    print("REGISTRAR VENDA")
    print("="*50)

    while True:
        try:
            produto_id_input = input("Digite o ID do produto (ou 0 para finalizar): ")
            if not produto_id_input.isdigit():
                print("ID inválido. Digite um número.")
                continue

            produto_id = int(produto_id_input)
            if produto_id == 0:
                print("Finalizando o registro de vendas.")
                break 

            produto = ProdutoService.buscar_produto_por_id(produto_id, produto_repo)
            if not produto:
                print(f"Produto ID {produto_id} não encontrado.")
                continue

            preco_unitario = produto.preco

            quantidade_input = input(f"Digite a quantidade de '{produto.nome}': ")
            if not quantidade_input.isdigit():
                print("Quantidade inválida. Digite um número inteiro positivo.")
                continue

            quantidade = int(quantidade_input)
            if quantidade <= 0:
                print("Quantidade deve ser um número positivo maior que zero.")
                continue

            data = input("Digite a data da venda (AAAA-MM-DD, deixe em branco para data atual): ")
            
            if not data:
                data = datetime.now().strftime('%Y-%m-%d')
            elif not re.match(r'\d{4}-\d{2}-\d{2}', data):
                print("Formato de data inválido. Use o formato AAAA-MM-DD.")
                continue

            try:
                datetime.strptime(data, '%Y-%m-%d')
            except ValueError:
                print("Data inválida. Verifique se o mês ou o dia são válidos.")
                continue

            if VendaService.registrar_venda(produto_id, quantidade, preco_unitario, data, venda_repo):
                print(f"Venda de {quantidade} unidades do produto ID {produto_id} registrada com sucesso!")
            else:
                print(f"Não foi possível registrar a venda para o produto ID {produto_id}.")

        except ValueError:
            print("Entrada inválida! Por favor, insira números válidos.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

def atualizar_venda(venda_repo: 'VendaRepository', produto_repo: 'ProdutoRepository'):
    """Permite ao usuário atualizar os dados de uma venda existente."""
    
    print("\n" + "="*50)
    print("ATUALIZAR VENDA")
    print("="*50)

    try:
        venda_id_input = input("Digite o ID da venda que deseja atualizar: ")
        if not venda_id_input.isdigit():
             print("ID inválido. Digite um número.")
             return
             
        venda_id = int(venda_id_input)
        
        venda = venda_repo.obter_venda_por_id(venda_id)
        
        if not venda:
            print("Venda não encontrada!")
            return
        
        print(f"\n--- Informações atuais da venda ---")
        print(f"ID Venda: {venda.id}")
        print(f"Produto ID: {venda.produto_id}")
        print(f"Quantidade: {venda.quantidade}")
        print(f"Data: {venda.data}")
        print(f"Total: R$ {venda.total:.2f}")
        print("-------------------------------------\n")
        
        novo_produto_id = input(f"Novo Produto ID (deixe em branco para manter {venda.produto_id}): ")
        nova_quantidade = input(f"Nova Quantidade (deixe em branco para manter {venda.quantidade}): ")
        nova_data = input(f"Nova Data (AAAA-MM-DD, deixe em branco para manter {venda.data}): ")

        novo_produto_id_final = int(novo_produto_id) if novo_produto_id and novo_produto_id.isdigit() else venda.produto_id
        nova_quantidade_final = int(nova_quantidade) if nova_quantidade and nova_quantidade.isdigit() else venda.quantidade
        nova_data_final = nova_data if nova_data else venda.data

        if VendaService.atualizar_venda(venda_id, novo_produto_id_final, nova_quantidade_final, nova_data_final, venda_repo):
            print(f"\nVenda atualizada com sucesso!")
        else:
             print(f"\nErro ao atualizar a venda. Verifique se o novo Produto ID existe.")

    except ValueError:
        print("❗ Entrada inválida. Por favor, insira os dados corretamente.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def deletar_venda(venda_repo: 'VendaRepository'):
    """Permite ao usuário deletar uma venda pelo ID."""
    
    print("\n" + "="*50)
    print("DELETAR VENDA")
    print("="*50)

    try:
        venda_id_input = input("Digite o ID da venda que deseja deletar: ")
        if not venda_id_input.isdigit():
             print("ID inválido. Digite um número.")
             return
             
        venda_id = int(venda_id_input)
        
        if VendaService.deletar_venda(venda_id, venda_repo):
            print(f"\nVenda ID {venda_id} deletada com sucesso!")
        else:
            print("Não foi possível deletar a venda.")
    
    except ValueError:
        print("❗ Entrada inválida. Por favor, insira um número para o ID da venda.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def imprimir_relatorios(produto_repo: 'ProdutoRepository'):
    """Gera e imprime todos os relatórios disponíveis."""
    
    print("\n" + "="*40)
    print("Relatório de Total de Vendas por Produto:")

    total_vendas = RelatorioService.total_vendas_por_produto(produto_repo) 
    for produto, total in total_vendas:
        print(f"{produto}: R${total:.2f}")
    salvar_relatorio_csv(total_vendas, 'relatorio_total_vendas.csv', ['Produto', 'Total de Vendas'])
    
    print("\n" + "="*40)
    print("Média de Preço dos Produtos:")
    
    media = RelatorioService.media_preco_produtos(produto_repo) 
    print(f"R${media:.2f}")
    
    salvar_relatorio_csv([("Média Geral", media)], 'relatorio_media_preco.csv', ['Descrição', 'Média de Preço'])
    
    print("\n" + "="*40)
    print("Produtos Mais Vendidos (Top 5):")
    
    mais_vendidos = RelatorioService.produtos_mais_menos_vendidos(produto_repo)
    for produto, total in mais_vendidos[:5]: 
        print(f"{produto}: {total} unidades")
    salvar_relatorio_csv(mais_vendidos[:5], 'relatorio_produtos_mais_vendidos.csv', ['Produto', 'Total Vendido'])
    
    print("\n" + "="*40)
    print("Vendas por Categoria:")
    vendas_categoria = RelatorioService.vendas_por_categoria(produto_repo)
    if vendas_categoria:
        for categoria, total in vendas_categoria:
            print(f"{categoria}: R${total:.2f}")
        salvar_relatorio_csv(vendas_categoria, 'relatorio_vendas_por_categoria.csv', ['Categoria', 'Total de Vendas'])
    else:
        print("Nenhuma venda registrada por categoria.")
