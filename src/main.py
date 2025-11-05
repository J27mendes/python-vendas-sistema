import sys
import os

# Adiciona o diretório 'src' ao sys.path para garantir que o Python consiga localizar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.RelatorioService import imprimir_relatorios
from utils.Database import criar_banco_de_dados
from repositories.ProdutoRepository import ProdutoRepository
from controllers.menu_views import (
    buscar_produtos_interativo,
    atualizar_produto,
    ver_vendas_interativo,
    registrar_venda_interativo,
    atualizar_venda,
    deletar_venda
)


def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Buscar Produto")
        print("2 - Atualizar Produto")
        print("3 - Ver Vendas")
        print("4 - Registrar Venda")
        print("5 - Atualizar venda") 
        print("6 - Deletar Venda")
        print("0 - Sair")
        
        opcao = input("Escolha a opção desejada: ")
        
        if opcao == "1":
            buscar_produtos_interativo()
        elif opcao == "2":
            atualizar_produto()
        elif opcao == "3":
            ver_vendas_interativo()
        elif opcao == "4":
            registrar_venda_interativo() 
        elif opcao == "5":
            atualizar_venda()
        elif opcao == "6":
            deletar_venda()
        elif opcao == "0":
            imprimir_relatorios()
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def main():
    criar_banco_de_dados()
    ProdutoRepository.carregar_dados_simulados()
    menu()

if __name__ == "__main__":
    main()
