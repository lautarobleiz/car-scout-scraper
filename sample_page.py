import requests

#Tomamos una url de ejemplo para saber cómo es la estructura de la página y, como consecuente la estructura de las publicaciones.
url = "https://www.autocosmos.com.ar/auto/usado/toyota/corolla"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)

print("Status code:", response.status_code)

with open("sample_page.html", "w", encoding="utf-8") as archivo:
    archivo.write(response.text)

print("HTML guardado en sample_page.html")