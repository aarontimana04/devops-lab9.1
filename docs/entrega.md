# Checklist de entrega

Documento fuente: `laboratorio-9.pdf`. La guía exige entrega en GitLab.
GitHub conserva código y evidencias por solicitud del alumno.

| Requisito | Estado real | Evidencia / acción |
| --- | --- | --- |
| URL GitHub | Preparado para publicación | aarontimana04/devops-lab9.1 |
| URL GitLab | Proyecto privado creado | aaron.timana/gitlab_lambda_demo |
| Código en GitLab | Pendiente | Autenticación Git y push |
| Acceso @pytuxi | Pendiente | Invitación Reporter autorizada |
| FastAPI + handler v2 | Verificado localmente | tests/test_hello.py, tests/test_handler.py |
| Tests | 16 pasan | evidencias/local/tests.log y test-results.xml |
| Coverage API/handler | 100 % | evidencias/local/coverage.xml; excluye inicio manual Uvicorn |
| Serverless v3 offline | Verificado localmente | evidencias/local/offline.log |
| /hello y /add JSON | Verificado localmente | hello.json, add.json, respuestas.log |
| Pipeline cinco jobs en verde | Pendiente | Captura Build > Pipelines |
| Runner laptop Online | Pendiente | Captura Settings > CI/CD > Runners |
| whoami en laptop | Pendiente | Log con nombre e ID del runner local |
| test en runner GitLab | Pendiente | Log con nombre e ID de instance runner |
| Imagen runner en Docker Desktop | Pendiente | Captura Images y contenedor runner |
| Terminal Server ready + curl | Logs verificados; captura pendiente | Terminal con servidor y JSON |
| Job offline con RESPUESTA /hello y /add | Script preparado; ejecución CI pendiente | Captura del log remoto |
| Artifacts pasados entre jobs | Configurado; CI pendiente | Informe generado por docs |
| Cache acelera ejecuciones | Configurado; no medido | Comparar primer y segundo pipeline |

Capturas sugeridas: `01-pipeline.png`, `02-runner-online.png`,
`03-whoami-laptop.png`, `04-test-gitlab.png`, `05-docker-runner.png`,
`06-offline-local.png`, `07-offline-job.png`. Guardarlas en `evidencias/capturas/`.
Deben corresponder a ejecuciones reales; no usar las imágenes de ejemplo del PDF.
