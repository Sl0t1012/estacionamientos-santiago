-- ============================================================
-- QUERIES DE ANÁLISIS — Estacionamientos Santiago
-- ============================================================

-- 1. Precio promedio por comuna (laboral)
SELECT
    c.nombre AS comuna,
    ROUND(AVG(p.precio_hora), 0) AS precio_promedio,
    ROUND(MIN(p.precio_hora), 0) AS precio_minimo,
    ROUND(MAX(p.precio_hora), 0) AS precio_maximo
FROM precios_por_hora p
JOIN estacionamientos e ON p.estacionamiento_id = e.id
JOIN comunas c ON e.comuna_id = c.id
WHERE p.tipo_dia = 'laboral'
GROUP BY c.nombre
ORDER BY precio_promedio DESC;

-- 2. Variación horaria por tipo de día
SELECT
    p.hora_inicio,
    p.tipo_dia,
    ROUND(AVG(p.precio_hora), 0) AS precio_promedio
FROM precios_por_hora p
GROUP BY p.hora_inicio, p.tipo_dia
ORDER BY p.hora_num, p.tipo_dia;

-- 3. Ranking precio vs seguridad (valor = precio bajo + seguridad alta)
SELECT
    c.nombre AS comuna,
    ROUND(AVG(p.precio_hora), 0) AS precio_promedio,
    c.score_seguridad,
    ROUND(c.score_seguridad / (AVG(p.precio_hora) / 1000), 3) AS indice_valor
FROM precios_por_hora p
JOIN estacionamientos e ON p.estacionamiento_id = e.id
JOIN comunas c ON e.comuna_id = c.id
WHERE p.tipo_dia = 'laboral'
GROUP BY c.nombre, c.score_seguridad
ORDER BY indice_valor DESC;

-- 4. Estacionamientos con mejor precio en horario peak (12-14h)
SELECT
    e.nombre,
    c.nombre AS comuna,
    e.tipo,
    ROUND(AVG(p.precio_hora), 0) AS precio_peak,
    CASE WHEN e.vigilancia = 1 THEN 'Sí' ELSE 'No' END AS tiene_guardia
FROM precios_por_hora p
JOIN estacionamientos e ON p.estacionamiento_id = e.id
JOIN comunas c ON e.comuna_id = c.id
WHERE p.hora_num BETWEEN 12 AND 14
  AND p.tipo_dia = 'laboral'
GROUP BY e.id
ORDER BY precio_peak ASC
LIMIT 20;

-- 5. Comparación tipo estacionamiento
SELECT
    e.tipo,
    ROUND(AVG(p.precio_hora), 0) AS precio_promedio,
    COUNT(DISTINCT e.id) AS cantidad
FROM precios_por_hora p
JOIN estacionamientos e ON p.estacionamiento_id = e.id
WHERE p.tipo_dia = 'laboral'
GROUP BY e.tipo
ORDER BY precio_promedio DESC;
