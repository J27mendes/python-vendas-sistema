import sqlite3
from src.utils.Database import obter_caminho_banco
from contextlib import contextmanager

class BaseRepository:
    """
    Classe base para Repositórios.
   
    """

    def __init__(self, table_name: str):
        """Inicializa o repositório com o nome da tabela que ele gerencia."""
        self.table_name = table_name

    @contextmanager
    def _conectar_db(self):
        """
        Gerenciador de contexto que abre e fecha a conexão ao banco.
        Retorna (conn, cursor).
        """
        conn = None
        try:
            db_path = obter_caminho_banco()
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            yield conn, cursor
        except sqlite3.Error as e:
            print(f"Erro de conexão/execução no banco de dados para {self.table_name}: {e}")
            # Em caso de erro, apenas imprime, mas garante o fechamento
        finally:
            if conn:
                conn.close()

    def deletar_generico(self, id: int):
        """
        Método polimórfico para deletar um registro usando o ID
        na tabela especificada no construtor.
        """
        try:
            with self._conectar_db() as (conn, cursor):
                # Se houver um erro de conexão, conn será None (por causa do 'finally')
                if conn is None:
                    return
                
                query = f"DELETE FROM {self.table_name} WHERE id = ?"
                cursor.execute(query, (id,))
                conn.commit()
                print(f"Registro ID {id} deletado com sucesso de {self.table_name}.")
        except Exception as e:
            print(f"Erro ao deletar registro na tabela {self.table_name}: {e}")