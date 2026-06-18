from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

# INICIALIZA O DRIVER

service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)

# FUNÇÕES DE SCRAPING

def pegar_preco_magalu(driver, produto):
    driver.get(f"https://www.magazineluiza.com.br/busca/{produto.replace(' ', '%20')}/")
    time.sleep(3)

    try:
        preco = driver.find_element(By.CSS_SELECTOR, "[data-testid='price-value']").text
        return preco
    except:
        return "Não encontrado"


def pegar_preco_amazon(driver, produto):
    driver.get(f"https://www.amazon.com.br/s?k={produto.replace(' ', '+')}")
    time.sleep(3)

    try:
        preco = driver.find_element(By.CSS_SELECTOR, ".a-price-whole").text
        return preco
    except:
        return "Não encontrado"


def pegar_preco_ml(driver, produto):
    driver.get(f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}")
    time.sleep(3)

    try:
        preco = driver.find_element(By.CSS_SELECTOR, ".andes-money-amount__fraction").text
        return preco
    except:
        return "Não encontrado"

# PRODUTO PESQUISADO

produto = "Macbook Air M5"

# COLETA DE PREÇOS 

preco_a = pegar_preco_magalu(driver, produto)
preco_b = pegar_preco_amazon(driver, produto)
preco_c = pegar_preco_ml(driver, produto)

# MONTA A TABELA FINAL
dados = [
    [produto, "Magazine Luiza", preco_a],
    [produto, "Amazon", preco_b],
    [produto, "Mercado Livre", preco_c]
]

# SALVA NO EXCEL
df = pd.DataFrame(dados, columns=["Produto", "Loja", "Preço"])
df.to_excel("comparacao_precos.xlsx", index=False)

#MOSTRAR RESULTADO
print("Comparação salva no Excel com sucesso!")

driver.quit()

