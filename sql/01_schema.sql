-- ============================================================
-- ESQUEMA: Análisis de Estacionamientos en Santiago
-- ============================================================

CREATE TABLE IF NOT EXISTS comunas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT NOT NULL UNIQUE,
    zona        TEXT,           -- 'oriente', 'centro', 'poniente', 'sur'
    score_seguridad REAL,       -- 0-10, derivado de datos CEAD
    poblacion   INTEGER
);

CREATE TABLE IF NOT EXISTS estacionamientos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT NOT NULL,
    direccion       TEXT,
    comuna_id       INTEGER REFERENCES comunas(id),
    tipo            TEXT,       -- 'superficie', 'subterraneo', 'mall', 'edificio'
    lat             REAL,
    lng             REAL,
    vigilancia      INTEGER DEFAULT 0,  -- 1 = tiene guardia
    techado         INTEGER DEFAULT 0,
    fuente          TEXT        -- 'scraping', 'google_maps', 'manual'
);

CREATE TABLE IF NOT EXISTS precios_por_hora (
    id                      INTEGER PRIMARY KEY AUTOINCREMENT,
    estacionamiento_id      INTEGER REFERENCES estacionamientos(id),
    hora_inicio             TEXT NOT NULL,  -- '08:00'
    hora_fin                TEXT NOT NULL,  -- '09:00'
    hora_num                INTEGER,        -- 8 (para ordenar en Power BI)
    precio_hora             REAL NOT NULL,
    tipo_dia                TEXT NOT NULL,  -- 'laboral', 'sabado', 'domingo'
    fecha_registro          TEXT DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS seguridad_comunal (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    comuna_id       INTEGER REFERENCES comunas(id),
    anio            INTEGER,
    delitos_total   INTEGER,
    tasa_por_10k    REAL,
    fuente          TEXT DEFAULT 'CEAD'
);

-- Índices para mejorar performance en Power BI
CREATE INDEX IF NOT EXISTS idx_precios_hora ON precios_por_hora(hora_num, tipo_dia);
CREATE INDEX IF NOT EXISTS idx_est_comuna ON estacionamientos(comuna_id);
