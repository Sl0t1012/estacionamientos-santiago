# Análisis de Estacionamientos en Santiago de Chile
### Precio, Ubicación y Seguridad Comunal

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![SQL](https://img.shields.io/badge/SQL-SQLite-lightgrey?logo=sqlite)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow?logo=powerbi)
![Claude AI](https://img.shields.io/badge/Claude_AI-Automatización-blueviolet)

---

## Descripción

Proyecto de análisis de datos que mapea los estacionamientos de las principales comunas de Santiago, cruzando **precio por hora**, **tipo de estacionamiento** y un **índice de seguridad comunal** derivado de datos del CEAD (Centro de Estudios y Análisis del Delito).

El objetivo es responder preguntas concretas para conductores y empresas:
- ¿Cuál es la relación precio/seguridad por comuna?
- ¿En qué horarios suben más los precios?
- ¿Qué comunas ofrecen mejor valor?

---

## Stack tecnológico

| Capa | Herramienta | Uso |
|---|---|---|
| Recolección | Python + BeautifulSoup | Web scraping de sitios y portales |
| Enriquecimiento | Claude AI (API) | Clasificación automática desde texto libre |
| Almacenamiento | SQLite / PostgreSQL | Esquema relacional normalizado |
| Transformación | Python (Pandas) | ETL, limpieza, score de seguridad |
| Visualización | Power BI | Dashboard interactivo publicado |

---

## Estructura del repositorio

```
estacionamientos-santiago/
│
├── data/
│   ├── raw/                  # Datos crudos del scraping (no subir a git)
│   └── processed/            # CSVs limpios listos para Power BI
│
├── sql/
│   ├── 01_schema.sql         # Creación de tablas
│   └── 02_queries_analisis.sql  # Queries de análisis documentados
│
├── src/
│   ├── scraping/
│   │   └── scraper.py        # Recolección de datos
│   ├── etl/
│   │   ├── transform.py      # Limpieza y transformación
│   │   └── generar_datos_ejemplo.py  # Dataset sintético para demo
│   └── ai/
│       └── claude_enrichment.py  # Integración con Claude API
│
├── notebooks/
│   └── 01_exploracion.ipynb  # EDA inicial
│
├── powerbi/
│   └── README_powerbi.md     # Guía de conexión y medidas DAX
│
├── docs/
│   └── arquitectura.md       # Diagrama y decisiones de diseño
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Instalación

```bash
git clone https://github.com/TU_USUARIO/estacionamientos-santiago.git
cd estacionamientos-santiago
pip install -r requirements.txt
```

Copia `.env.example` a `.env` y agrega tu API key de Claude:

```bash
cp .env.example .env
# Edita .env con tu ANTHROPIC_API_KEY
```

---

## Cómo ejecutar

**1. Generar datos de ejemplo (sin necesidad de scraping real):**
```bash
python src/etl/generar_datos_ejemplo.py
```

**2. Cargar schema SQL:**
```bash
sqlite3 data/processed/estacionamientos.db < sql/01_schema.sql
```

**3. Correr el enriquecimiento con Claude AI:**
```bash
python src/ai/claude_enrichment.py
```

**4. Conectar Power BI** al archivo `data/processed/precios_por_hora.csv`

---

## Hallazgos principales

> Dataset de ejemplo — reemplazar con datos reales al publicar.

- Las Condes presenta los precios más altos con peak a las 13:00 (~$1.800/hr en día laboral)
- Santiago Centro ofrece mejor relación precio/seguridad en horario nocturno
- Los domingos los precios caen hasta un 35% respecto al día laboral
- Estacionamientos subterráneos cobran en promedio 20% más que los de superficie

---

## Dashboard Power BI

📊 [Ver dashboard publicado](https://app.powerbi.com/TU_LINK) ← *(actualizar al publicar)*

Páginas del dashboard:
1. Portada con KPIs ejecutivos
2. Mapa de calor comunal (precio + seguridad)
3. Variación de precios por hora
4. Ranking de estacionamientos por relación precio-valor

---

## Fuentes de datos

- Datos de precios: scraping de portales de estacionamiento + Google Maps API
- Índice de seguridad comunal: [CEAD Chile](http://cead.spd.gov.cl/)
- Límites comunales: datos abiertos del INE

---

## Autor

**Gonzalo Vergara Espinoza**
Analista de Sistemas | Data Analyst

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Gonzalo_Vergara-blue?logo=linkedin)](https://www.linkedin.com/in/TU_PERFIL)
[![GitHub](https://img.shields.io/badge/GitHub-TU_USUARIO-black?logo=github)](https://github.com/TU_USUARIO)

---

## Licencia

MIT — libre para usar y adaptar con atribución.
