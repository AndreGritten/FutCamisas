import json
from datetime import datetime
import os

CAMINHO_RELATORIOS = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'relatorios_vendas.json')

def registrar_venda_em_arquivo(venda_id, cliente_nome, data_hora_venda, produtos_vendidos, valor_total):
    registro = {
        "id_venda": venda_id,
        "cliente_nome": cliente_nome,
        "data_hora": data_hora_venda,
        "produtos": produtos_vendidos,
        "valor_total": valor_total
    }

    registros_existentes = []
    if os.path.exists(CAMINHO_RELATORIOS) and os.path.getsize(CAMINHO_RELATORIOS) > 0:
        with open(CAMINHO_RELATORIOS, 'r', encoding='utf-8') as f:
            try:
                registros_existentes = json.load(f)
            except json.JSONDecodeError:
                registros_existentes = []

    registros_existentes.append(registro)

    with open(CAMINHO_RELATORIOS, 'w', encoding='utf-8') as f:
        json.dump(registros_existentes, f, indent=4, ensure_ascii=False)

    print(f"Venda {venda_id} registrada em relatorios_vendas.json")

def ler_relatorios():
    if not os.path.exists(CAMINHO_RELATORIOS) or os.path.getsize(CAMINHO_RELATORIOS) == 0:
        return []
    with open(CAMINHO_RELATORIOS, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []