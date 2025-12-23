from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import os
import csv
from datetime import datetime

# Inicializando o driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.vivareal.com.br/venda/rio-grande-do-sul/sao-leopoldo/")

driver.implicitly_wait(10) 

# Aceitando os cookies
botao_cookies = driver.find_element(By.CLASS_NAME, 'cookie-notifier__cta')
botao_cookies.click()

# Criando uma pasta para armazenar os screenshots
os.makedirs("screenshots", exist_ok=True)

# Encontrando todos os elementos de anúncios
anuncios = driver.find_elements(By.CSS_SELECTOR, 'div[data-type="property"]')

# Verificando se o arquivo CSV já existe
file_exists = os.path.isfile("historico_anuncios.csv")

# Abrindo arquivo CSV para escrita
with open("historico_anuncios.csv", mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if not file_exists:
        writer.writerow(["Data", "URL", "Local", "Preço", "Screenshot"])

    for i, anuncio in enumerate(anuncios):
        # Obtendo a URL do anúncio
        try:
            url = anuncio.find_element(By.CSS_SELECTOR, 'a.property-card__content-link.js-card-title').get_attribute("href")
        except:
            url = "URL não encontrada"
        
        # Obtendo o local do anúncio
        try:
            local = anuncio.find_element(By.CLASS_NAME, "property-card__address").text
        except:
            local = "Local não encontrado"
        
        # Obtendo o preço do anúncio
        try:
            preco = anuncio.find_element(By.CLASS_NAME, "property-card__price").text
        except:
            preco = "Preço não encontrado"

        print(f"URL: {url}")
        print(f"Local: {local}")
        print(f"Preço: {preco}")
        print("-" * 50)

        # Salvando o screenshot do anúncio
        screenshot_path = f"screenshots/anuncio_{i + 1}.png"
        anuncio.screenshot(screenshot_path)
        print(f"Screenshot salvo em: {screenshot_path}")

        # Escrevendo os dados no CSV
        writer.writerow(
            [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                url,
                local,
                preco,
                screenshot_path,
            ]
        )

driver.quit()
