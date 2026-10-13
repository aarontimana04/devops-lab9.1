"""Inicia offline, verifica JSON y guarda logs reales. No usa AWS."""
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import time
import urllib.error
import urllib.request


def get_json(path):
    with urllib.request.urlopen("http://127.0.0.1:3000" + path, timeout=8) as response:
        return json.load(response)


def main():
    output = Path(os.environ.get("EVIDENCE_DIR", "evidencias/local"))
    output.mkdir(parents=True, exist_ok=True)
    # No dar por válida la respuesta de otro servidor que ocupe nuestros puertos.
    for port in (3000, 3002):
        with socket.socket() as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(("127.0.0.1", port))
    with (output / "offline.log").open("w") as log:
        process = subprocess.Popen(
            ["./node_modules/.bin/serverless", "offline"],
            stdout=log, stderr=subprocess.STDOUT, process_group=0,
        )
        try:
            deadline = time.monotonic() + 90
            while True:
                if process.poll() is not None:
                    raise RuntimeError("Serverless terminó; revisar offline.log")
                try:
                    if get_json("/hello").get("message") == "Hello, World!":
                        break
                except (OSError, urllib.error.URLError):
                    pass
                if time.monotonic() > deadline:
                    raise TimeoutError("La API no estuvo lista en 90 segundos")
                time.sleep(1)
            results = []
            for route, filename, expected in [
                ("/hello?name=Aaron", "hello.json",
                 {"message": "Hello, Aaron!", "source": "FastAPI"}),
                ("/add?a=2&b=3", "add.json", {"result": 5}),
            ]:
                payload = get_json(route)
                if payload != expected:
                    raise AssertionError(f"Respuesta inesperada: {payload!r}")
                encoded = json.dumps(payload, ensure_ascii=False)
                (output / filename).write_text(encoded + "\n")
                line = f"RESPUESTA {route.split('?')[0]}: {encoded}"
                print(line, flush=True)
                results.append(line)
            try:
                get_json("/add?a=x&b=3")
                raise AssertionError("Se esperaba HTTP 422")
            except urllib.error.HTTPError as error:
                if error.code != 422:
                    raise
            (output / "respuestas.log").write_text("\n".join(results) + "\nHTTP 422 validado\n")
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
    print("Smoke test offline: OK", flush=True)


if __name__ == "__main__":
    main()
