import sys
import os

# Adiciona o diretório 'src' ao sys.path para garantir que o Python consiga localizar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.ProdutoService import ProdutoService
from src.services.VendaService import VendaService
from src.utils.Database import criar_banco_de_dados
from src.services.RelatorioService import imprimir_relatorios


def main():
   criar_banco_de_dados()

   ProdutoService.listar_produtos_e_ids()
    
   ProdutoService.carregar_dados_simulados()

   vendas = VendaService.registrar_venda()

   if vendas:
      # Registra as vendas no banco de dados (chamada estática)
      VendaService.registrar_vendas(vendas)
      print("\nVendas registradas. Gerando relatórios...")
      imprimir_relatorios() 
   else:
      print("Nenhuma venda foi registrada.")

   print("\n" + "="*50)
   print("🛒 REGISTRO DE VENDAS")
   print("="*50)

if __name__ == "__main__":
    main()