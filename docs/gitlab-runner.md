# Configuración GitLab y runner Docker

Proyecto creado: https://gitlab.com/aaron.timana/gitlab_lambda_demo

## 1. Subir el código

La sesión web de GitLab está autenticada mediante SSO. Git por HTTPS necesita
un token con `write_repository` o una clave SSH configurada por el propietario.
No guardar tokens en archivos del repo, capturas, URLs o mensajes de chat.

Con autenticación Git ya configurada:

```bash
git remote add gitlab https://gitlab.com/aaron.timana/gitlab_lambda_demo.git
git push -u gitlab main
```

Si el remoto ya existe, usar `git remote -v` para comprobarlo.
El primer pipeline puede quedar pending hasta que se registre el runner local.

## 2. Dar acceso al docente

Manage > Members > Invite members. Buscar `@pytuxi` y verificar su perfil.
Para revisar código privado y pipelines basta el rol **Reporter**.
No se ha enviado esta invitación; debe autorizarla el propietario.

## 3. Crear el runner en GitLab

Settings > CI/CD > Runners > New project runner:

- Sistema Linux: el proceso runner y sus jobs corren en contenedores Linux,
  aunque Docker Desktop esté instalado en macOS.
- Tag: `laptop`.
- Desmarcar **Run untagged jobs**.
- Descripción: `laptop-aaron-lab9`.
- Copiar el token de autenticación `glrt-...` de forma privada.

La imagen oficial `gitlab/gitlab-runner` aparecerá en Docker Desktop. El montaje
del socket Docker permite al runner crear los contenedores de los jobs; supone
acceso administrativo al daemon Docker de la laptop. Usarlo solo para este
proyecto y mantener `runner/config/` fuera de Git (ya está ignorado).

## 4. Iniciar y registrar

Abrir Docker Desktop y esperar que el engine esté listo:

```bash
docker info
docker compose -f runner/compose.yml up -d
# Registro interactivo: ingresar el token cuando el comando lo solicite.
docker compose -f runner/compose.yml exec gitlab-runner gitlab-runner register
```

Responder URL `https://gitlab.com`, token privado, executor `docker` e imagen
por defecto `python:3.11`. Mantener el nombre indicado por GitLab.

```bash
docker compose -f runner/compose.yml exec gitlab-runner gitlab-runner verify
docker compose -f runner/compose.yml logs --tail=50
docker ps
```

La comprobación decisiva es el runner **Online** en la interfaz y el job
`whoami` mostrando `Runner: laptop-aaron-lab9`. `verify` solo comprueba que
el registro puede contactar con GitLab; no demuestra que un job se ejecutó.

## 5. Habilitar instance runners y ejecutar

En Settings > CI/CD > Runners, habilitar los instance runners. GitLab puede
pedir verificación de identidad o tener cuotas; debe completarlo el propietario.
`test`, `offline`, `package` y `docs` no llevan tags. El runner local no debe
aceptar jobs sin tags para que estos se ejecuten en GitLab.

Build > Pipelines > New pipeline > `main`. Esperar los cinco jobs en verde.
No modificar los tags para presentar una ejecución local como shared runner.

## 6. Capturar evidencia

Revisar `docs/entrega.md`. En el log de `test`, anotar el nombre e ID del runner
GitLab y compararlos con `whoami`. Descargar artifacts del job `docs`.

La laptop debe seguir encendida y Docker ejecutándose mientras corre `whoami`.
Los contenedores de los jobs son efímeros. Los volúmenes de builds/cache e
imágenes pueden permanecer después de terminar; una imagen sin contenedor
activo no indica que el job no se ejecutó.

Para detener únicamente este runner:

```bash
docker compose -f runner/compose.yml stop
```
