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
El runner local está registrado y Online, y el docente tiene acceso Reporter.
Se conservan capturas reales de ambos estados. El código se guardó también en GitLab. Después de que el titular verificó
su identidad, el pipeline 2941167512 aprobó los cinco jobs. Sus artifacts
se descargaron y verificaron localmente.
La condición Online se verificó en GitLab. No se han inventado jobs en verde.

El ZIP contiene fuentes y requirements, no dependencias binarias para Lambda.
El empaquetado desplegable, credenciales AWS y Serverless v4 corresponden al
laboratorio de Bitbucket mencionado por el docente.

También se ejecutaron las 16 pruebas en Docker Linux/arm64 con Python 3.11,
con 100 % de cobertura. Los resultados están en `python311-tests.log`,
`python311-test-results.xml` y `python311-coverage.xml`.

## Evidencia remota final

- Pipeline: https://gitlab.com/aaron.timana/gitlab_lambda_demo/-/pipelines/2941167512
- whoami: job 17130257923, runner laptop-aaron-lab9 (ID 57342024).
- test: job 17130257924, runner k8s.saas-linux-small-amd64 de GitLab.
- offline: job 17130257925, JSON correctos de /hello y /add.
- package: job 17130257926, ZIP íntegro con fuentes.
- docs: job 17130257927, recibió artifacts de test, offline y package.
- Duración total publicada por GitLab: 2 minutos 23 segundos.
- JUnit remoto: 16 pruebas, cero errores y fallos; cobertura 100 %.

El paquete de artifacts se conserva en evidencias/ci/artifacts-docs.zip.
La segunda ejecución 2941199447 también aprobó los cinco jobs. Los logs de
los jobs test (17130479805) y offline (17130479806) muestran Successfully
extracted cache para pip y npm. El tiempo total pasó de 2:23 a 2:12; esa
diferencia observada no se atribuye exclusivamente a la cache porque los
runners y sus tiempos de preparación pueden variar.

Segunda ejecución: https://gitlab.com/aaron.timana/gitlab_lambda_demo/-/pipelines/2941199447
