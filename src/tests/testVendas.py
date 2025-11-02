import unittest
from unittest.mock import patch, MagicMock
from src.services.ProdutoService import ProdutoService
from src.services.VendaService import VendaService
from src.models.Produto import Produto 

class TestSistemaVendas(unittest.TestCase):

    # ----------------------------------------------------
    # TESTE 1: CADASTRAR PRODUTO 
    # ----------------------------------------------------
    # O patch mira no ProdutoRepository importado dentro do ProdutoService

    @patch('src.services.ProdutoService.ProdutoRepository')
    def test_cadastrar_produto(self, MockProdutoRepository):
        """Testa se o ProdutoService cria o objeto Produto e chama o Repositório corretamente."""
        
        # 1. Preparação
        produto_service = ProdutoService()
        nome = "Produto Mockado"
        categoria = "Cat Mock"
        preco = 99.99
        
        # 2. Execução
        produto_service.cadastrar_produto(nome, categoria, preco)
        
        # 3. Verificação (Assertion):
        
        MockProdutoRepository.criar_produto.assert_called_once()
        
        # call_args[0][0] pega o primeiro argumento posicional da primeira chamada
        produto_passado = MockProdutoRepository.criar_produto.call_args[0][0]
        
        # Verifica se o objeto é um Produto e se seus atributos estão corretos
        self.assertIsInstance(produto_passado, Produto)
        self.assertEqual(produto_passado.nome, nome, "O nome do produto criado está incorreto.")
        self.assertEqual(produto_passado.categoria, categoria, "A categoria do produto criado está incorreta.")
        self.assertEqual(produto_passado.preco, preco, "O preço do produto criado está incorreto.")
