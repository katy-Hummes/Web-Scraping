from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv
from datetime import datetime

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.vilarica.com.br/comprar/prontos/sao-leopoldo-rs")

driver.implicitly_wait(10) 

botao_cookies = driver.find_element(By.CLASS_NAME, 'lgpd-accept')
botao_cookies.click()

# Criando uma pasta para armazenar os screenshots
os.makedirs("screenshots", exist_ok=True)

anuncios = driver.find_elements(By.CLASS_NAME, "wrap-link")

file_exists = os.path.isfile("historico_anuncios_vila_rica.csv")

# Abrindo arquivo CSV para escrita
with open("historico_anuncios.csv", mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Data", "URL", "Local", "Preço", "Screenshot"])

    for i, anuncio in enumerate(anuncios):
        url = anuncio.get_attribute("href")
        try:
            local = anuncio.find_element(
                By.XPATH, ".//p[@class='location']"
            ).text
        except:
            local = "Local não encontrado"
        try:
            preco = anuncio.find_element(By.XPATH, ".//p[@class='price']").text
        except:
            preco = "Preço não encontrado"

        print(f"URL: {url}")
        print(f"Local: {local}")
        print(f"Preço: {preco}")
        print("-" * 50)

        screenshot_path = f"screenshots/anuncio_{i + 1}.png"
        anuncio.screenshot(screenshot_path)
        print(f"Screenshot salvo em: {screenshot_path}")

        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                url,
                local,
                preco,
                screenshot_path,
            ]
        )

        # Verificando URLs
for i, anuncio in enumerate(anuncios):
    url = anuncio.get_attribute("href")
    if url and url.startswith("https://www.vilarica.com.br/comprar/pronto/"):
        try:
            local = anuncio.find_element(
                By.XPATH, ".//p[@class='location']"
            ).text
        except:
            local = "Local não encontrado"
        try:
            preco = anuncio.find_element(By.XPATH, ".//p[@class='price']").text
        except:
            preco = "Preço não encontrado"

        print(f"URL: {url}")
        print(f"Local: {local}")
        print(f"Preço: {preco}")
        print("-" * 50)

        # Capturando o screenshot do elemento
        screenshot_path = f"screenshots/anuncio_{i + 1}.png"
        anuncio.screenshot(screenshot_path)
        print(f"Screenshot salvo em: {screenshot_path}")

        # Escrevendo dados no CSV
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                url, 
                local, 
                preco, 
                screenshot_path, 
            ]
        )
    else:
        print(f"URL inválida: {url}")

driver.quit()