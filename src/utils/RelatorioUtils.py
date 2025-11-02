import csv
from typing import List, Tuple

def salvar_relatorio_csv(dados: List[Tuple], nome_arquivo: str, cabecalho: List[str]):
    """Função para salvar os relatórios em arquivos CSV (atualizando, não sobrescrevendo)"""
    try:
        with open(nome_arquivo, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # Se o arquivo estiver vazio, escreve o cabeçalho
                writer.writerow(cabecalho)
            writer.writerows(dados)
    except Exception as e:
        print(f"Erro ao salvar o CSV: {e}")