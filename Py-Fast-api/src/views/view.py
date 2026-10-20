"""Interfaz interactiva de consola para consumir la API de aprendices."""

import json
import os

import httpx

DEFAULT_API_URL = "https://apis-python.onrender.com"
REQUEST_TIMEOUT_SECONDS = 90.0

TRAINEE_FIELDS = (
    ("document", "Documento"),
    ("firstname", "Nombres"),
    ("lastname", "Apellidos"),
    ("email", "Correo electrónico"),
    ("age", "Edad"),
    ("program", "Programa"),
    ("record_number", "Número de ficha"),
)


class ApiClient:
    """Cliente HTTP pequeño para las rutas CRUD existentes."""

    def __init__(self, base_url: str, timeout: float = REQUEST_TIMEOUT_SECONDS):
        self.base_url = base_url.strip().rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=timeout,
            headers={"Accept": "application/json"},
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self._client.close()

    def request(self, method: str, path: str, **kwargs) -> httpx.Response | None:
        try:
            response = self._client.request(method, path.lstrip("/"), **kwargs)
        except httpx.RequestError as error:
            print(f"No fue posible conectar con la API: {error}")
            print(f"Dirección configurada: {self.base_url}")
            return None

        if response.is_error:
            try:
                detail = response.json()
            except ValueError:
                detail = response.text or response.reason_phrase
            print(f"La API respondió HTTP {response.status_code}:")
            print(json.dumps(detail, ensure_ascii=False, indent=2))
            return None

        return response


def show_response(response: httpx.Response | None):
    if response is None:
        return
    if not response.content:
        print("Operación completada.")
        return
    try:
        result = response.json()
    except ValueError:
        result = response.text
    print(json.dumps(result, ensure_ascii=False, indent=2))


def ask_required(label: str) -> str:
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("Este campo es obligatorio.")


def ask_integer(label: str) -> int:
    while True:
        value = input(f"{label}: ").strip()
        try:
            return int(value)
        except ValueError:
            print("Ingresa un número entero.")


def prompt_new_trainee() -> dict:
    print("\nDatos del aprendiz nuevo")
    payload = {}
    for field, label in TRAINEE_FIELDS:
        if field in {"age", "record_number"}:
            payload[field] = ask_integer(label)
        else:
            payload[field] = ask_required(label)
    return payload


def prompt_trainee_update() -> dict:
    print("\nDeja vacío cada campo que quieras conservar sin cambios.")
    payload = {}
    for field, label in TRAINEE_FIELDS:
        if field == "document":
            continue
        value = input(f"{label} (opcional): ").strip()
        if not value:
            continue
        if field in {"age", "record_number"}:
            try:
                payload[field] = int(value)
            except ValueError:
                print(f"{label} debe ser un número entero.")
                return {}
        else:
            payload[field] = value
    return payload


def list_trainees(client: ApiClient):
    show_response(client.request("GET", "/trainees"))


def get_trainee(client: ApiClient):
    trainee_id = ask_required("ID del aprendiz")
    show_response(client.request("GET", f"/trainee/{trainee_id}"))


def create_trainee(client: ApiClient):
    show_response(client.request("POST", "/trainee", json=prompt_new_trainee()))


def update_trainee(client: ApiClient):
    trainee_id = ask_required("ID del aprendiz")
    payload = prompt_trainee_update()
    if not payload:
        print("No se enviaron cambios.")
        return
    show_response(client.request("PUT", f"/trainee/{trainee_id}", json=payload))


def delete_trainee(client: ApiClient):
    trainee_id = ask_required("ID del aprendiz")
    confirmation = input(
        f"¿Confirmas eliminar el aprendiz {trainee_id}? Escribe S para continuar: "
    ).strip()
    if confirmation.lower() != "s":
        print("Eliminación cancelada.")
        return
    show_response(client.request("DELETE", f"/trainee/{trainee_id}"))


def main():
    base_url = os.environ.get("API_BASE_URL", DEFAULT_API_URL)
    print("API de gestión de aprendices")
    print(f"Servidor: {base_url.rstrip('/')}")

    try:
        with ApiClient(base_url) as client:
            while True:
                print(
                    "\n"
                    "1. Listar aprendices\n"
                    "2. Consultar aprendiz por ID\n"
                    "3. Crear aprendiz\n"
                    "4. Actualizar aprendiz\n"
                    "5. Eliminar aprendiz\n"
                    "0. Salir"
                )
                option = input("Selecciona una opción: ").strip()
                actions = {
                    "1": list_trainees,
                    "2": get_trainee,
                    "3": create_trainee,
                    "4": update_trainee,
                    "5": delete_trainee,
                }
                if option == "0":
                    print("Hasta luego.")
                    return
                action = actions.get(option)
                if action is None:
                    print("Opción no válida. Selecciona del 0 al 5.")
                    continue
                try:
                    action(client)
                except (EOFError, KeyboardInterrupt):
                    print("\nOperación cancelada.")
    except (httpx.InvalidURL, ValueError) as error:
        print(f"La URL de la API no es válida: {error}")


if __name__ == "__main__":
    main()
