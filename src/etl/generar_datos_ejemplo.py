"""
Genera un dataset sintético de estacionamientos para Santiago.
Útil para demostrar el pipeline sin datos reales.
"""
import pandas as pd
import sqlite3
import itertools
import os

COMUNAS = {
    'Las Condes':      {'zona': 'oriente',  'score_seguridad': 7.2, 'precio_base': 1400},
    'Providencia':     {'zona': 'oriente',  'score_seguridad': 6.8, 'precio_base': 1250},
    'Santiago Centro': {'zona': 'centro',   'score_seguridad': 5.1, 'precio_base': 1100},
    'Ñuñoa':           {'zona': 'oriente',  'score_seguridad': 6.5, 'precio_base': 950},
    'Vitacura':        {'zona': 'oriente',  'score_seguridad': 8.1, 'precio_base': 1600},
    'Maipú':           {'zona': 'poniente', 'score_seguridad': 5.8, 'precio_base': 750},
    'La Florida':      {'zona': 'sur',      'score_seguridad': 5.4, 'precio_base': 800},
}

TIPOS_DIA    = ['laboral', 'sabado', 'domingo']
TIPOS_EST    = ['superficie', 'subterraneo', 'mall']
HORAS        = list(range(7, 23))

FACTOR_HORA  = {h: (1.3 if 12 <= h <= 14 else 0.8 if h < 9 or h > 20 else 1.0) for h in HORAS}
FACTOR_DIA   = {'laboral': 1.0, 'sabado': 0.9, 'domingo': 0.75}
FACTOR_TIPO  = {'subterraneo': 1.2, 'mall': 1.1, 'superficie': 1.0}


def generar_precios() -> pd.DataFrame:
    rows = []
    for (comuna, info), hora, tipo_dia, tipo_est in itertools.product(
            COMUNAS.items(), HORAS, TIPOS_DIA, TIPOS_EST):
        precio = round(
            info['precio_base']
            * FACTOR_HORA[hora]
            * FACTOR_DIA[tipo_dia]
            * FACTOR_TIPO[tipo_est]
            / 50
        ) * 50
        rows.append({
            'comuna':               comuna,
            'hora':                 f'{hora:02d}:00',
            'hora_num':             hora,
            'tipo_dia':             tipo_dia,
            'tipo_estacionamiento': tipo_est,
            'precio_hora':          precio,
            'score_seguridad':      info['score_seguridad'],
            'zona':                 info['zona'],
        })
    return pd.DataFrame(rows)


def guardar_csv(df: pd.DataFrame, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False, encoding='utf-8-sig')
    print(f"CSV guardado: {path} ({len(df):,} filas)")


def guardar_sqlite(df: pd.DataFrame, db_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql('precios_por_hora', conn, if_exists='replace', index=False)
    print(f"SQLite guardado: {db_path}")


if __name__ == '__main__':
    df = generar_precios()
    guardar_csv(df, 'data/processed/precios_por_hora.csv')
    guardar_sqlite(df, 'data/processed/estacionamientos.db')

    print("\nResumen por comuna (laboral):")
    resumen = (df[df.tipo_dia == 'laboral']
               .groupby('comuna')['precio_hora']
               .agg(['mean', 'min', 'max'])
               .round(0)
               .sort_values('mean', ascending=False))
    print(resumen.to_string())
