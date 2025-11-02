import sys
import os

# Adiciona o diretório 'src' ao sys.path para garantir que o Python consiga localizar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.ProdutoService import ProdutoService
from src.utils.Database import criar_banco_de_dados


def main():
   criar_banco_de_dados()
    
   ProdutoService.carregar_dados_simulados()

if __name__ == "__main__":
    main()