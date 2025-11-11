import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..')) 
sys.path.insert(0, project_root)

import unittest
from unittest.mock import patch, MagicMock
from src.services.ProdutoService import ProdutoService
from src.services.VendaService import VendaService
from src.models.Produto import Produto 
from src.models.Venda import Venda

class TestSistemaVendas(unittest.TestCase):

    # ----------------------------------------------------
    # TESTE 1: CADASTRAR PRODUTO 
    # ----------------------------------------------------
    
    @patch('src.repositories.ProdutoRepository.ProdutoRepository')
    def test_cadastrar_produto(self, MockProdutoRepositoryClass):
        """Testa se o ProdutoService cria o objeto Produto e chama o Repositório corretamente."""
        
        # 1. Preparação: Cria uma instância mock do Repositório 
        mock_repo_instance = MockProdutoRepositoryClass.return_value
        
        nome = "Produto Mockado"
        categoria = "Cat Mock"
        preco = 99.99
        
        # 2. Execução: Chama o método estático e INJETA o mock como dependência
        ProdutoService.cadastrar_produto(nome, categoria, preco, mock_repo_instance)
        
        # 3. Verificação (Assertion):
        mock_repo_instance.criar_produto.assert_called_once()
        
        # call_args[0][0] pega o primeiro argumento posicional da primeira chamada
        produto_passado = mock_repo_instance.criar_produto.call_args[0][0]
        
        # Verifica se o objeto é um Produto e se seus atributos estão corretos
        self.assertIsInstance(produto_passado, Produto)
        self.assertEqual(produto_passado.nome, nome, "O nome do produto criado está incorreto.")
        self.assertEqual(produto_passado.categoria, categoria, "A categoria do produto criado está incorreta.")
        self.assertEqual(produto_passado.preco, preco, "O preço do produto criado está incorreto.")

    # ----------------------------------------------------
    # TESTE 2: REGISTRAR VENDA 
    # ----------------------------------------------------
    
    @patch('src.repositories.VendaRepository.VendaRepository')
    def test_registrar_venda_chama_adicionar_corretamente(self, MockVendaRepositoryClass):
        """
        Testa se o VendaService calcula o total e chama o método 'adicionar' do Repositório.
        """
        
        # 1. Preparação
        mock_repo_instance = MockVendaRepositoryClass.return_value
        produto_id = 1
        quantidade = 5
        preco_unitario = 10.00
        data = '2025-11-01'
        total_esperado = 50.00 # 5 * 10.00

        # 2. Execução: Chama o método estático e INJETA o mock.
        VendaService.registrar_venda(produto_id, quantidade, preco_unitario, data, mock_repo_instance)

        # 3. Verificação
        mock_repo_instance.criar_venda.assert_called_once()
        
        venda_passada = mock_repo_instance.criar_venda.call_args[0][0]
        
        self.assertIsInstance(venda_passada, Venda)
        self.assertEqual(venda_passada.produto_id, produto_id)
        self.assertEqual(venda_passada.quantidade, quantidade)
        self.assertEqual(venda_passada.data.isoformat(), data) # Verifica a data como string ISO
        self.assertEqual(venda_passada.total, total_esperado)

    # ----------------------------------------------------
    # TESTE 3: DELETAR VENDA 
    # ----------------------------------------------------
    
    @patch('src.repositories.VendaRepository.VendaRepository')
    @patch('src.services.VendaService.print') 
    def test_deletar_venda_chama_deletar_corretamente(self, MockPrint, MockVendaRepositoryClass):
        """
        Testa se o VendaService: 1. Busca a venda (obter_venda_por_id). 2. Deleta o registro (deletar_generico).
        """
        
        # 1. Preparação
        mock_repo_instance = MockVendaRepositoryClass.return_value
        venda_id = 5
        
        # Mockar a checagem de existência:
        mock_venda_obj = MagicMock()
        mock_repo_instance.obter_venda_por_id.return_value = mock_venda_obj
        
        # 2. Execução
        resultado = VendaService.deletar_venda(venda_id, mock_repo_instance)

        # 3. Verificação (Assertion)
        
        # O Service deve checar a existência
        mock_repo_instance.obter_venda_por_id.assert_called_once_with(venda_id)
        
        # chama o Service
        mock_repo_instance.deletar_generico.assert_called_once_with(venda_id)
        
        self.assertTrue(resultado, "A deleção deve retornar True.")
   

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False) # Adicionado argv/exit para evitar problemas em alguns IDEs