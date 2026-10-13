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
| Pipeline cinco jobs en verde | Bloqueado por identidad | Pipeline 2941149714; 09-bloqueo-verificacion.png |
| Runner laptop Online | Verificado en GitLab | 02-runner-online.png, ID 57342024 |
| whoami en laptop | Pendiente | Log con nombre e ID del runner local |
| test en runner GitLab | Pendiente | Log con nombre e ID de instance runner |
| Imagen runner en Docker Desktop | Verificado | 05-docker-runner.png |
| Terminal Server ready + curl | Servidor y JSON verificados; captura de terminal pendiente | offline.log y 06-offline-local.png (navegador) |
| Job offline con RESPUESTA /hello y /add | Script preparado; ejecución CI pendiente | Captura del log remoto |
| Artifacts pasados entre jobs | Configurado; CI pendiente | Informe generado por docs |
| Cache acelera ejecuciones | Configurado; no medido | Comparar primer y segundo pipeline |

Capturas sugeridas: `01-pipeline.png`, `02-runner-online.png`,
`03-whoami-laptop.png`, `04-test-gitlab.png`, `05-docker-runner.png`,
`06-offline-local.png`, `07-offline-job.png`. Guardarlas en `evidencias/capturas/`.
Deben corresponder a ejecuciones reales; no usar las imágenes de ejemplo del PDF.

## Bloqueo externo observado

GitLab exige al titular verificar su identidad antes de ejecutar pipelines.
El pipeline [2941149714](https://gitlab.com/aaron.timana/gitlab_lambda_demo/-/pipelines/2941149714)
se creó para el commit `51c7f62a7cdeb2195aaece6db5d116acff2f818b`, pero no ejecutó
los jobs. La pantalla mostró "Verify your identity to run this pipeline".
La verificación se completa en https://gitlab.com/-/identity_verification.
Después, crear un nuevo pipeline de main y verificar cada job y sus artifacts.
