# Informe de desarrollo - Laboratorio 9.1

## Objetivo y solución

Se implementó una API REST FastAPI con dos rutas: `/hello` saluda a un nombre y
`/add` suma dos enteros. FastAPI valida parámetros y responde HTTP 422 cuando
una suma recibe texto o falta un operando. Mangum permite invocar la misma
aplicación con un evento de API Gateway HTTP API v2, sin duplicar la lógica.

Serverless Framework 3.40.0 y serverless-offline 13.9.0 simulan API Gateway y
Lambda en la laptop. Las versiones están fijadas y `package-lock.json` permite
usar `npm ci`. Se mantuvo v3 según el alcance de la guía; no se desplegó a AWS.

## Pruebas realizadas

El 13 de octubre de 2026 se ejecutaron 16 pruebas en macOS con Python 3.12.14.
Se probaron funciones puras, HTTP, validación, eventos Lambda v2, nombres con
Unicode y caracteres de URL, y una ruta inexistente (404). Todas pasaron.
La cobertura de la API y el handler es 100 %, excluyendo el arranque interactivo
de Uvicorn. Ruff no encontró errores en los archivos Python.

El smoke test inició Serverless offline con Node 24 y el Python del entorno
virtual. Verificó `/hello?name=Aaron`, `/add?a=2&b=3` y HTTP 422 para `a=x`.
Las respuestas reales y las invocaciones Lambda se guardaron en evidencias.
Se verificó también el ZIP de código fuente mediante `ZipFile.testzip()`.

## Decisiones del pipeline

Se conservaron los stages `info`, `test`, `offline`, `package`, `docs`.
`whoami` tiene el tag `laptop`. El job `test` espera al stage info sin `needs`.
Los jobs posteriores declaran sus dependencias con `needs`; `package` y `docs`
reciben y verifican artifacts reales de jobs anteriores. Los resultados de
pytest se publican como JUnit y la cobertura como Cobertura.

Cache pip/npm y artifacts tienen propósitos diferentes: cache reutiliza
paquetes descargados entre ejecuciones; artifacts transporta resultados y el
ZIP entre jobs. Sus claves incluyen los archivos de dependencias para evitar
reutilizar entradas incompatibles cuando cambian las versiones.

## Límites de la evidencia

La validación local se completó. La validación YAML local comprueba sintaxis y
tipos de scripts, pero no reemplaza CI Lint ni la ejecución GitLab.
El pipeline remoto, el registro del runner, la invitación al docente y sus
capturas siguen pendientes de autorización/autenticación de GitLab.
No se han inventado jobs en verde ni evidencias de un runner Online.

El ZIP contiene fuentes y requirements, no dependencias binarias para Lambda.
El empaquetado desplegable, credenciales AWS y Serverless v4 corresponden al
laboratorio de Bitbucket mencionado por el docente.
