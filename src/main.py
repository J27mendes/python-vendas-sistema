import sys
import os

# Adiciona o diretório 'src' ao sys.path para garantir que o Python consiga localizar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.Produto import Produto 
from src.services.ProdutoService import ProdutoService
from src.services.VendaService import VendaService
from src.utils.Database import criar_banco_de_dados
from src.services.RelatorioService import imprimir_relatorios

def buscar_produto_interativo():
    """Permite ao usuário buscar um produto pelo ID via input."""
    
    print("\n" + "="*50)
    print("BUSCA DE PRODUTO POR ID")
    print("exemplo de busca: 1 = A, 2 = B, 3 = C, 4 = D, 5 = E, 6 = F, os exemplos  7 , 8, 9 são destinados a testes!")
    print("="*50)
    
    while True:
        try:
            # 1. Coleta a entrada do usuário
            entrada = input("Digite entre 1 e 6 o ID do produto que deseja buscar (ou 0 para sair): ")

            
            produto_id = int(entrada)
            
            if produto_id == 0:
                print("Encerrando busca.")
                break
                
            if produto_id < 0:
                print("O ID deve ser um número positivo.")
                continue

            produto: Produto = ProdutoService.buscar_produto_por_id(produto_id)
            
            # 3. Exibe o resultado
            if produto:
                print("\n--- Produto Encontrado ---")
                print(f"ID: {produto.id}")
                print(f"Nome: {produto.nome}")
                print(f"Categoria: {produto.categoria}")
                print(f"Preço: R$ {produto.preco:.2f}")
                print("--------------------------\n")
            # O serviço já imprime a mensagem "Não encontrado" se o produto for None
                
        except ValueError:
            # Captura se o usuário digitar texto
            print("❗ Entrada inválida. Por favor, digite apenas números inteiros (ID).")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")


def main():
   criar_banco_de_dados()

   ProdutoService.listar_produtos_e_ids()
    
   ProdutoService.carregar_dados_simulados()

   buscar_produto_interativo()

   vendas = VendaService.registrar_venda()

   print("\n" + "="*50)
   print("🛒 REGISTRO DE VENDAS")
   print("="*50)

   if vendas:
      # Registra as vendas no banco de dados (chamada estática)
      VendaService.registrar_vendas(vendas)
      print("\nVendas registradas. Gerando relatórios...")
      imprimir_relatorios() 
   else:
      print("Nenhuma venda foi registrada.")

if __name__ == "__main__":
    main()