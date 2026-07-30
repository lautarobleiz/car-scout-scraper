import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.autocosmos.com.ar"

#URL de prueba, luego se hace dinamico en base a lo que el usuario busque. Pero eso cuando avancemos con car scout.
URL_BUSQUEDA = "https://www.autocosmos.com.ar/auto/usado/toyota/corolla"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def obtener_html(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()  #Lanza error si el status no es 200
    return response.text

def parsear_autos(html):
    soup = BeautifulSoup(html, "lxml")
    articulos = soup.find_all("article", class_="listing-card") #Es donde estan los autos

    autos = []
    for art in articulos:
        try:
            marca = art.find(itemprop="brand").text.strip()
            modelo = art.find(class_="listing-card__model").text.strip()
            version = art.find(class_="listing-card__version").text.strip()
            anio = int(art.find(itemprop="modelDate").text.strip())

            km_texto = art.find(itemprop="mileageFromOdometer").text.strip()
            km = int(km_texto.replace("km", "").strip())

            ciudad = art.find(itemprop="addressLocality").text.replace("|", "").strip()
            provincia = art.find(itemprop="addressRegion").text.strip()

            moneda = art.find(itemprop="priceCurrency")["content"]
            precio = int(art.find(itemprop="price")["content"])

            href = art.find("a", itemprop="url")["href"]
            url_original = BASE_URL + href

            id_externo = href.rstrip("/").split("/")[-1]

            auto = {
                "fuente": "autocosmos",
                "id_externo": id_externo,
                "marca": marca,
                "modelo": modelo,
                "version": version,
                "anio": anio,
                "km": km,
                "precio": precio,
                "moneda": moneda,
                "ciudad": ciudad,
                "provincia": provincia,
                "url_original": url_original,
            }
            autos.append(auto)

        except AttributeError as e:
            print(f"Error parseando el auto con id externo [{id_externo}]: {e}")
            continue

    return autos


if __name__ == "__main__":
    html = obtener_html(URL_BUSQUEDA)
    autos = parsear_autos(html)

    print(f"Se encontraron {len(autos)} autos.\n")
    for auto in autos[:3]:  #Mostramos solo los primeros 3 de prueba
        print(auto)
        print("---")