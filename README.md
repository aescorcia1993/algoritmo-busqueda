# algoritmo-busqueda
Entrenamiento de inteligencia Artificial en Python

Se implemento un sistema de busqueda de rutas para transporte masivo usando:

- UCS (Uniform Cost Search) como algoritmo principal para encontrar la mejor ruta por costo total.
- BFS como linea base para comparar contra una busqueda no ponderada.
- Reglas logicas sobre la base de conocimiento para restringir el recorrido.

### Reglas logicas incluidas

- No pasar por estaciones cerradas.
- No usar lineas cerradas.
- Evitar estaciones congestionadas (si esta activado).
- Penalizar transbordos para priorizar rutas mas directas.
- Limitar costo total maximo (opcional).

## Estructura

- `main.py`: implementacion de grafo, reglas, UCS, BFS y casos de prueba.

## Requisitos

- Python 3.10+ (sin librerias externas).

## Ejecucion

Desde la raiz del proyecto:

```bash
python3 main.py
```

## Salida esperada

El script ejecuta 3 escenarios:

1. Operacion normal.
2. Estacion cerrada.
3. Evitar congestion + linea cerrada.

En cada caso se muestra:

- Ruta obtenida por UCS.
- Costo total acumulado.
- Detalle por tramos (linea y tiempo).
- Numero de transbordos.
- Ruta encontrada por BFS para comparacion.

```text
======================================================================
Caso 1: Operacion normal
======================================================================
Ruta UCS: PortalNorte -> Suba -> Sur
Costo total (minutos + penalizacion): 18
Detalle:
   PortalNorte --[L2/8m]--> Suba
   Suba --[L2/10m]--> Sur
Transbordos: 0
Ruta BFS (minimo numero de estaciones): PortalNorte -> Suba -> Sur
======================================================================
Caso 2: Estacion Centro cerrada
======================================================================
Ruta UCS: PortalNorte -> Suba -> Sur
Costo total (minutos + penalizacion): 18
Detalle:
   PortalNorte --[L2/8m]--> Suba
   Suba --[L2/10m]--> Sur
Transbordos: 0
Ruta BFS (minimo numero de estaciones): PortalNorte -> Suba -> Sur
======================================================================
Caso 3: Evitar congestion y linea L1 cerrada
======================================================================
UCS: No existe ruta valida para las reglas actuales.
BFS: No existe ruta valida para las reglas actuales.
```
