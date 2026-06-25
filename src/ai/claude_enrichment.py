"""
Enriquecimiento de datos con Claude AI.
Toma descripciones en texto libre de estacionamientos y extrae
atributos estructurados: tipo, servicios, cobertura, etc.
"""
import json
import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """Eres un extractor de datos especializado en estacionamientos urbanos.
A partir de una descripción en texto libre, extrae los atributos en JSON.
Responde SOLO con el JSON, sin texto adicional."""

SCHEMA = {
    "tipo": "superficie | subterraneo | mall | edificio | calle",
    "techado": "true | false",
    "vigilancia_24h": "true | false",
    "acepta_mensual": "true | false",
    "servicios": ["lavado", "valet", "carga_electrica"],
    "confianza": "alta | media | baja"
}


def clasificar_estacionamiento(descripcion: str) -> dict:
    """Extrae atributos estructurados de una descripción de texto libre."""
    prompt = f"""Descripción del estacionamiento:
\"\"\"{descripcion}\"\"\"

Esquema esperado:
{json.dumps(SCHEMA, ensure_ascii=False, indent=2)}

Extrae los atributos disponibles. Para campos sin información, usa null."""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
        system=SYSTEM_PROMPT,
    )

    raw = message.content[0].text.strip()
    return json.loads(raw)


def generar_resumen_hallazgos(stats: dict) -> str:
    """Genera un párrafo narrativo con los hallazgos para el dashboard."""
    prompt = f"""Eres un analista de datos. Escribe UN párrafo ejecutivo (máx 80 palabras)
en español con los hallazgos clave del análisis de estacionamientos en Santiago.
Usa los datos proporcionados. Sé directo y orientado a insights accionables.

Datos:
{json.dumps(stats, ensure_ascii=False, indent=2)}"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


if __name__ == '__main__':
    # Ejemplo de clasificación
    ejemplos = [
        "Estacionamiento subterráneo 24 horas con guardia de seguridad. Acepta abono mensual. Carga para vehículos eléctricos.",
        "Playa de estacionamiento al aire libre, sin vigilancia, disponible solo días de semana de 8 a 20 hrs.",
        "Parking techado en centro comercial, entrada por Av. Apoquindo. Valet disponible fines de semana.",
    ]

    print("=== Clasificación con Claude AI ===\n")
    for desc in ejemplos:
        print(f"Descripción: {desc[:60]}...")
        resultado = clasificar_estacionamiento(desc)
        print(f"Resultado:   {json.dumps(resultado, ensure_ascii=False)}\n")

    # Ejemplo de resumen narrativo
    stats_ejemplo = {
        "precio_promedio_laboral": 1240,
        "comuna_mas_cara": "Vitacura ($1.720/hr)",
        "comuna_mejor_valor": "Santiago Centro (precio bajo + seguridad media)",
        "variacion_fin_semana": "-30%",
        "tipo_mas_caro": "subterráneo (20% sobre superficie)"
    }

    print("=== Narrativa automática para dashboard ===\n")
    resumen = generar_resumen_hallazgos(stats_ejemplo)
    print(resumen)
