# Car Scout — Scraper

Módulo de scraping del proyecto **Car Scout**, una plataforma de comparación de precios de autos usados en Argentina. Este repositorio se encarga de recolectar publicaciones de distintos portales de venta de autos, normalizarlas a un formato común y almacenarlas para su posterior consumo por el backend de Car Scout.

## Sobre el proyecto

Car Scout agrega publicaciones de autos usados de varias fuentes argentinas (mediante scraping y APIs), normaliza los datos y compara precios y características entre ellas, para que el usuario pueda elegir la opción que mejor se ajuste a lo que busca.

Este repo es únicamente la capa de **recolección de datos**: corre de forma independiente y periódica, sin intervenir en tiempo real en las búsquedas de los usuarios finales.

## Fuentes de datos

| Fuente | Método | Estado |
|---|---|---|
| Autocosmos | Scraping | ✅ Implementado |
| Kavak | Scraping | 🔜 Planeado |
| deRuedas | Scraping | 🔜 Planeado |
| Autos.com.ar | Scraping | 🔜 Planeado |
| MercadoLibre | API oficial | 🔜 Planeado |

> **Nota:** MercadoLibre y OLX no se scrapean — su `robots.txt` lo prohíbe explícitamente. MercadoLibre se integra en cambio mediante su API oficial.

## Stack técnico

- **Python** 3.9+
- **requests** — obtención de HTML
- **BeautifulSoup** (parser `lxml`) — parseo de HTML
- **SQLite** — almacenamiento (migración a PostgreSQL planeada)

## Instalación

### Requisitos previos
- Python 3.9 o superior
- Git

### Pasos

```bash
# Clonar el repositorio
git clone https://github.com/TU-USUARIO/car-scout-scraper.git
cd car-scout-scraper

# Crear entorno virtual
python3 -m venv venv          # Windows: python -m venv venv

# Activar entorno virtual
source venv/bin/activate      # Windows (PowerShell): venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

## Uso

```bash
python3 scraper.py
```

Esto ejecuta el scraper de Autocosmos, guarda los resultados en `car_scout.db` (SQLite) y muestra un resumen en consola.

## Estructura de la base de datos

- **`autos`** — datos fijos de cada publicación (marca, modelo, año, km, ubicación, fuente, etc.), con restricción `UNIQUE(fuente, id_externo)` para evitar duplicados en corridas sucesivas
- **`precios_historicos`** — un registro nuevo por cada vez que se detecta el precio de un auto, para mantener un historial de precios en el tiempo

## Arquitectura

- **Patrón adapter**: cada fuente normaliza sus datos a un formato canónico común antes de guardarlos, independientemente de si el origen es scraping o una API
- **Verificación diferida**: en vez de re-scrapear toda la base constantemente, se verifica la disponibilidad de una publicación solo cuando un usuario la consulta activamente
- **Selectores basados en microdatos `schema.org`** (`itemprop`) en lugar de clases CSS, por ser más estables ante cambios de diseño del sitio fuente
