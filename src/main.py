import sys
import os

from src.utils.Database import criar_banco_de_dados
from src.repositories.ProdutoRepository import ProdutoRepository
from src.repositories.VendaRepository import VendaRepository 
from src.controllers.menu_views import (
    buscar_produtos_interativo,
    atualizar_produto,
    ver_vendas_interativo,
    registrar_venda_interativo,
    atualizar_venda,
    deletar_venda,
    imprimir_relatorios 
)

produto_repository = ProdutoRepository()
venda_repository = VendaRepository() 

def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Buscar Produto")
        print("2 - Atualizar Produto")
        print("3 - Ver Vendas")
        print("4 - Registrar Venda")
        print("5 - Atualizar venda") 
        print("6 - Deletar Venda")
        print("7 - Imprimir Relatórios") 
        print("0 - Sair")
        
        opcao = input("Escolha a opção desejada: ")
        
        if opcao == "1":
            buscar_produtos_interativo(produto_repository)
        elif opcao == "2":
            atualizar_produto(produto_repository)
        elif opcao == "3":
            ver_vendas_interativo(venda_repository)
        elif opcao == "4":
            registrar_venda_interativo(venda_repository, produto_repository) 
        elif opcao == "5":
            atualizar_venda(venda_repository, produto_repository) 
        elif opcao == "6":
            deletar_venda(venda_repository)
        elif opcao == "7": 
            imprimir_relatorios(produto_repository)
        elif opcao == "0":
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    criar_banco_de_dados()
    produto_repository.carregar_dados_simulados() 
    menu()

if __name__ == "__main__": 
    main()