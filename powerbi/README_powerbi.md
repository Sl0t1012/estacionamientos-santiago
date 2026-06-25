# Power BI — Guía de conexión y medidas DAX

## Conexión al CSV

1. Abrir Power BI Desktop
2. Obtener datos → Texto/CSV
3. Seleccionar `data/processed/precios_por_hora.csv`
4. En Power Query, verificar tipos de columna:
   - `hora_num` → Número entero
   - `precio_hora` → Número decimal
   - `hora` → Texto (ordenar por `hora_num`)

**Importante:** seleccionar columna `hora`, ir a Herramientas de columna → Ordenar por columna → `hora_num`

---

## Medidas DAX principales

```dax
Precio Promedio =
AVERAGE(precios_por_hora[precio_hora])

Precio Máximo Hora =
MAXX(
    SUMMARIZE(precios_por_hora, precios_por_hora[hora], "avg", AVERAGE(precios_por_hora[precio_hora])),
    [avg]
)

Hora Pico =
VAR t = ADDCOLUMNS(VALUES(precios_por_hora[hora_num]), "p", CALCULATE(AVERAGE(precios_por_hora[precio_hora])))
RETURN MAXX(TOPN(1, t, [p], DESC), precios_por_hora[hora])

Variacion vs Hora Anterior =
VAR h = SELECTEDVALUE(precios_por_hora[hora_num])
RETURN DIVIDE(
    AVERAGE(precios_por_hora[precio_hora]) -
    CALCULATE(AVERAGE(precios_por_hora[precio_hora]), precios_por_hora[hora_num] = h - 1),
    CALCULATE(AVERAGE(precios_por_hora[precio_hora]), precios_por_hora[hora_num] = h - 1)
)

Indice Valor Comunal =
DIVIDE(
    AVERAGE(precios_por_hora[score_seguridad]),
    AVERAGE(precios_por_hora[precio_hora]) / 1000
)
```

---

## Páginas del dashboard

| # | Página | Visuales |
|---|---|---|
| 1 | Portada KPIs | 4 tarjetas métricas + segmentadores |
| 2 | Mapa comunal | Mapa de burbujas + tabla ranking |
| 3 | Variación horaria | Gráfico de líneas por hora |
| 4 | Precio vs seguridad | Dispersión + tabla top 10 |
