# algoritmo-busqueda
Entrenamiento de inteligencia Artificial en Python


Descripción de la actividad
Detalles
Estimados estudiantes, bienvenidos a la tercera  actividad del curso.

La siguiente actividad pretende acercar a los estudiantes a los sistemas inteligentes basados en conocimiento en particular utilizando estrategias de búsqueda y la representación del conocimiento a partir de reglas escritas en lenguaje lógico.

Para el desarrollo de este ejercicio debe tenerse en cuenta:

1. La actividad se podrá realizar en equipos de máximo 3 estudiantes. 

Se aconseja que realice las siguientes lecturas para complementar la información de la actividad (Clic para abrir la bibliografía de la unidad .)
2. Explorar los recursos de conocimiento para el desarrollo de la actividad y los recursos de apoyo sugeridos: capítulo 2 ( lógica y representación del conocimiento), capítulo 3 (Sistemas basados en reglas) y capítulo 9 (técnicas basadas en búsquedas heurísticas) del libro: 

Benítez, R. (2014). Inteligencia artificial avanzada. Barcelona: Editorial UOC. 
3. Escribir en Python las instrucciones para el desarrollo de un sistema inteligente que a partir de una base de conocimiento escrito en reglas lógicas, desarrolle la mejor ruta para moverse desde un punto A y un punto B en el sistema de transporte masivo local.

4. Desarrollar un corto video explicando el proyecto, los comandos realizados y los resultados obtenidos.

5. Subir la actividad en el enlace que corresponde para la entrega de la tarea, indicando el link del repositorio Git y del video.

Entregable:

Entregable: un documento PDF con el link a los siguientes elementos que estarán alojados en el repositorio Git o GitLab, donde deberán agregar al tutor como colaborador del proyecto con el fin de que pueda revisar el código y hacer comentarios.

Código fuente en Python y sus instrucciones para su ejecución.
Documento PDF con las pruebas realizadas 
Video (máximo 5 minutos) explicando el proyecto, los comandos realizados y los resultados obtenidos. El video debe ser claro y preciso, adicionalmente deben participar todos los integrantes del equipo.
El log del repositorio Git debe evidenciar el trabajo realizado por cada integrante del equipo.

## Implementacion propuesta (Opcion 3)

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

## Evidencias sugeridas para el PDF

- Captura de ejecucion del caso normal.
- Captura del caso con restricciones (estacion o linea cerrada).
- Comparacion corta: por que UCS da mejor ruta en costo que BFS en escenarios ponderados.

## Guion corto para el video (max. 5 min)

1. Presentar el problema y el modelo del grafo (estaciones y lineas).
2. Explicar las reglas logicas implementadas.
3. Mostrar ejecucion del programa.
4. Comparar UCS vs BFS rapidamente.
5. Concluir por que UCS cumple el criterio de mejor ruta en este proyecto.
