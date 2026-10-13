# Laboratorio 9.1 - GitLab CI/CD, FastAPI y Lambda

Autor: Aarón Timaná Castro. Curso: DevOps. Fecha: 13 de octubre de 2026.

- Código y evidencias: https://github.com/aarontimana04/devops-lab9.1
- Proyecto GitLab creado: https://gitlab.com/aaron.timana/gitlab_lambda_demo
- Guía del docente: https://github.com/utec-devops-2026/laboratorios/blob/main/laboratorio_gitlab/guia_gitlab_ci_runner.md

## Estado comprobado

La API y el handler pasan **16 pruebas**. La cobertura de `hello.py` y `handler.py`
es **100 %**, excluyendo el bloque que inicia Uvicorn manualmente.
`serverless offline` respondió a `/hello` y `/add`, y devolvió HTTP 422 para
un parámetro inválido. Las evidencias reales están en `evidencias/local/`.

El runner local está registrado y Online (ID 57342024). `@pytuxi` tiene acceso
Reporter. El código y el pipeline ya están subidos a GitLab. Su ejecución está bloqueada
por la verificación de identidad que exige GitLab al titular de la cuenta. Una prueba local no demuestra
un pipeline en verde. Revisar [checklist de entrega](docs/entrega.md).

## Qué hace cada componente

```mermaid
flowchart LR
    C[curl o navegador] --> S[Serverless offline :3000]
    S --> E[Evento API Gateway v2]
    E --> M[handler.py / Mangum]
    M --> F[FastAPI / hello.py]
    F --> R[Respuesta JSON]
```

`hello.py` define `greet`, `add` y las rutas. Mangum adapta el evento Lambda a ASGI.
Serverless v3 y el plugin offline simulan Lambda y API Gateway en la laptop.
Este laboratorio no despliega a AWS ni necesita credenciales AWS o Serverless.

## Instalar y ejecutar

Usar Python **3.11 o 3.12** y Node **20 a 24**. El pipeline utiliza Python 3.11
con Node 20; la comprobación local inicial usó Python 3.12 y Node 24.

```bash
git clone https://github.com/aarontimana04/devops-lab9.1.git
cd devops-lab9.1
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
npm ci
```

En macOS, ejecutar offline en una terminal real: el plugin v13 abre `/dev/tty`.
El entorno virtual debe estar activo: offline llama al `python3` del PATH.

```bash
npx serverless offline
```

En otra terminal:

```bash
curl -fsS 'http://localhost:3000/hello?name=Aaron'
# {"message":"Hello, Aaron!","source":"FastAPI"}
curl -fsS 'http://localhost:3000/add?a=2&b=3'
# {"result":5}
```

Para usar FastAPI sin simular Lambda: `python hello.py`. Swagger queda en
http://localhost:8000/docs. Serverless offline solo publica las dos rutas
configuradas en `serverless.yml`.

## Verificación reproducible

```bash
source .venv/bin/activate
ruff check hello.py handler.py tests scripts
pytest -v --junitxml=test-results.xml --cov=hello --cov=handler --cov-report=xml --cov-report=html --cov-fail-under=90
# Detener primero cualquier instancia offline que ocupe 3000/3002.
python scripts/smoke_offline.py
python scripts/package_app.py
```

El smoke test arranca su propio servidor, espera hasta 90 segundos, compara
JSON completos, verifica HTTP 422 y detiene los procesos que inició.
Guarda `offline.log` (servidor), `hello.json`, `add.json` y `respuestas.log`.
`RESPUESTA /hello` y `RESPUESTA /add` aparecen en el log del job, no solo en el
artifact del servidor.

El ZIP `dist/app-source.zip` es un paquete de **código fuente**, como en la guía.
Incluye API, handler, requirements y configuración; no contiene dependencias
instaladas y no se presenta como un ZIP listo para desplegar a Lambda.

## Pipeline

| Job | Stage | Runner previsto | Resultado/artifact |
| --- | --- | --- | --- |
| `whoami` | info | Laptop, tag `laptop` | Descripción, ID, tags, arquitectura |
| `test` | test | Instance runner GitLab | Lint, JUnit, coverage, HTML |
| `offline` | offline | Instance runner GitLab | JSON, logs, HTTP 422 |
| `package` | package | Instance runner GitLab | ZIP de código fuente |
| `docs` | docs | Instance runner GitLab | Informe con commit/pipeline y artifacts |

El runner local debe tener tag `laptop` y **Run untagged jobs desmarcado**.
Así `test`, que no tiene tags, va a un instance runner habilitado.
Sin esta configuración no basta con que el job carezca de tags.

`test` no tiene `needs`: espera al stage `info`. `offline` usa `needs: test`.
`package` espera a test y offline; `docs` recibe artifacts de los tres jobs.
`needs: []` permitiría que un job arranque inmediatamente, sin esperar stages
anteriores. En este caso se conserva el orden solicitado por el laboratorio.

La cache almacena descargas de pip/npm entre pipelines, con claves basadas en
los archivos de dependencias. Los artifacts conservan resultados de un job y
los pasan a los jobs consumidores; no cumplen la misma función que la cache.
No se comparte `.venv` ni `node_modules` entre máquinas.

## GitLab y runner

Seguir [configuración paso a paso](docs/gitlab-runner.md). GitHub conserva este
trabajo; el pipeline del laboratorio se ejecuta en GitLab con `.gitlab-ci.yml`.
No sustituir las capturas GitLab por un workflow GitHub Actions.

## Estructura

```text
.gitlab-ci.yml          pipeline de cinco jobs
hello.py               API y funciones puras
handler.py             adaptador Lambda
serverless.yml         rutas API Gateway v2 y runtime
package.json           Serverless 3.40.0, offline 13.9.0
package-lock.json      instalación reproducible npm ci
requirements*.txt      dependencias producción/desarrollo
tests/                 pruebas API y eventos Lambda
scripts/               smoke test y empaquetado
runner/compose.yml     runner en Docker Desktop
docs/                  guía, informe y checklist
evidencias/local/      resultados de ejecución reales
```
