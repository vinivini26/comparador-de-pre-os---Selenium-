# scrapers.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils import limpar_preco

def buscar_magalu(driver, produto):
    url = f"https://www.magazineluiza.com.br/busca/{produto.replace(' ', '%20')}/"
    driver.get(url)

    try:
        preco = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='price-value']"))
        ).text

        return ("Magazine Luiza", limpar_preco(preco))

    except:
        return ("Magazine Luiza", None)


def buscar_amazon(driver, produto):
    url = f"https://www.amazon.com.br/s?k={produto.replace(' ', '+')}"
    driver.get(url)

    try:
        preco = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".a-price-whole"))
        ).text

        return ("Amazon", limpar_preco(preco))

    except:
        return ("Amazon", None)


def buscar_mercadolivre(driver, produto):
    url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
    driver.get(url)

    try:
        preco = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".andes-money-amount__fraction"))
        ).text

        return ("Mercado Livre", limpar_preco(preco))

    except:
        return ("Mercado Livre", None)