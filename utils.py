import re

def limpar_preco(texto):
    if not texto:
        return None

    numero = re.findall(r'[\d.,]+', texto)

    return numero[0] if numero else None
