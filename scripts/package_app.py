"""ZIP de código fuente, como en la guía; no es un despliegue Lambda."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

Path("dist").mkdir(exist_ok=True)
with ZipFile("dist/app-source.zip", "w", ZIP_DEFLATED) as archive:
    for name in ("hello.py", "handler.py", "requirements.txt", "serverless.yml"):
        archive.write(name)
with ZipFile("dist/app-source.zip") as archive:
    assert archive.testzip() is None
    assert "handler.py" in archive.namelist()
print("ZIP verificado: dist/app-source.zip (código fuente; dependencias no incluidas)")
