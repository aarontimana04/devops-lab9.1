# Checklist de entrega

Documento fuente: `laboratorio-9.pdf`. La guía exige entrega en GitLab.
GitHub conserva código y evidencias por solicitud del alumno.

| Requisito | Estado real | Evidencia / acción |
| --- | --- | --- |
| URL GitHub | Publicado y verificado | aarontimana04/devops-lab9.1 |
| URL GitLab | Proyecto privado creado | aaron.timana/gitlab_lambda_demo |
| Código en GitLab | Guardado mediante la interfaz | Rama main, commit 51c7f62a |
| Acceso @pytuxi | Verificado en GitLab | 08-acceso-docente.png, rol Reporter |
| FastAPI + handler v2 | Verificado localmente | tests/test_hello.py, tests/test_handler.py |
| Tests | 16 pasan | evidencias/local/tests.log y test-results.xml |
| Coverage API/handler | 100 % | evidencias/local/coverage.xml; excluye inicio manual Uvicorn |
| Serverless v3 offline | Verificado localmente | evidencias/local/offline.log |
| /hello y /add JSON | Verificado localmente | hello.json, add.json, respuestas.log |
| Pipeline cinco jobs en verde | Verificado en GitLab | Pipeline 2941167512; 01-pipeline.png |
| Runner laptop Online | Verificado en GitLab | 02-runner-online.png, ID 57342024 |
| whoami en laptop | Verificado en GitLab | 03-whoami-laptop.png; evidencias/ci/whoami.log |
| test en runner GitLab | Verificado en GitLab | 04-test-gitlab.png; evidencias/ci/test.log |
| Imagen runner en Docker Desktop | Verificado | 05-docker-runner.png |
| Terminal Server ready + curl | Servidor y JSON verificados; captura de terminal pendiente | offline.log y 06-offline-local.png (navegador) |
| Job offline con RESPUESTA /hello y /add | Verificado en GitLab | 07-offline-job.png y offline-job.log |
| Artifacts pasados entre jobs | Descargados y verificados | artifacts-docs.zip e informe-pipeline.md |
| Cache pip/npm | Restauración verificada | Segunda ejecución 2941199447; cache-pip.log y cache-npm-pip.log |

Capturas sugeridas: `01-pipeline.png`, `02-runner-online.png`,
`03-whoami-laptop.png`, `04-test-gitlab.png`, `05-docker-runner.png`,
`06-offline-local.png`, `07-offline-job.png`. Guardarlas en `evidencias/capturas/`.
Deben corresponder a ejecuciones reales; no usar las imágenes de ejemplo del PDF.

## Resultado remoto

Pipeline 2941167512: cinco jobs aprobados. El primer intento 2941149714 quedó
bloqueado por identidad; el titular completó la verificación y se lanzó una
ejecución nueva. La captura 09 conserva ese antecedente, no el estado actual.

Se descargó el artifact del job docs y se verificó el ZIP, las fuentes del
paquete, 16 tests con cero fallos, cobertura 100 % y ambos JSON. Los prefijos
de tokens de los logs se omiten al publicarlos en GitHub.

La captura de la API local en navegador está guardada. Falta únicamente la
captura literal de la terminal local con Server ready; el funcionamiento
está acreditado por offline.log y las respuestas reales.
