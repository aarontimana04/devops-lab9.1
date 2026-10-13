"""Mangum convierte eventos API Gateway v2 en peticiones ASGI."""
from mangum import Mangum
from hello import app

handler = Mangum(app)
