# ui/services/api.py
import httpx

BASE_URL = "http://127.0.0.1:8080"  # ajustá si usás otro puerto
TIMEOUT = 10

_client = httpx.Client(base_url=BASE_URL, timeout=TIMEOUT)

def login(usuario: str, password: str) -> dict:
    # Cambiá la ruta si tu backend usa otra
    r = _client.post("/api/auth/login", json={"usuario": usuario, "password": password})
    r.raise_for_status()
    return r.json()

def clientes_list(q: str | None = None, page: int = 1, size: int = 25) -> dict:
    r = _client.get("/api/clientes", params={"q": q, "page": page, "size": size})
    r.raise_for_status()
    return r.json()
