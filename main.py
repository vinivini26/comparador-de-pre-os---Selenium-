from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
from datetime import datetime
import os

from scrapers import (
    buscar_magalu,
    buscar_amazon,
    buscar_mercadolivre
)

# DRIVER
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)


# CONFIGURAÇÃO HISTÓRICO
ARQUIVO_HISTORICO = "historico.xlsx"

# cria arquivo se não existir
if not os.path.exists(ARQUIVO_HISTORICO):
    df_init = pd.DataFrame(columns=["Data", "Produto", "Loja", "Preço"])
    df_init.to_excel(ARQUIVO_HISTORICO, index=False)

print("  ROBÔ DE COMPARAÇÃO DE PREÇOS")


# LOOP PRINCIPAL
while True:

    produto = input("\nDigite o produto (ou 'sair'): ").strip()

    if produto.lower() == "sair":
        print("Encerrando sistema...")
        break

    if not produto:
        print("Produto inválido.")
        continue

    print(f"\nBuscando: {produto}\n")

    sites = [
        buscar_magalu,
        buscar_amazon,
        buscar_mercadolivre
    ]

    resultados = []
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for site in sites:
        loja, preco = site(driver, produto)

        print(f"{loja}: {preco}")

        resultados.append([data_atual, produto, loja, preco])

    
    # SALVAR HISTÓRICO 
    df_novo = pd.DataFrame(resultados, columns=["Data", "Produto", "Loja", "Preço"])

    df_antigo = pd.read_excel(ARQUIVO_HISTORICO)

    df_final = pd.concat([df_antigo, df_novo], ignore_index=True)

    df_final.to_excel(ARQUIVO_HISTORICO, index=False)

    print("\nBusca salva no histórico.\n")

driver.quit()