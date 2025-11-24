from typing import Dict, Any

class ValidationMapper:
    """
    Validador de claves foráneas utilizando los repositorios inyectados.
    """
    def __init__(self, repositories: Dict[str, Any]):
        # repositories es un dict donde los valores son Providers (Factory) de dependency_injector
        self._repos = repositories

    def validate_fk_exists(self, repo_key: str, fk_id: int, fk_name: str) -> bool:
        if not fk_id or fk_id <= 0:
            print(f"Validación: {fk_name} debe ser un ID positivo.")
            return False

        repo_provider = self._repos.get(repo_key)
        if not repo_provider:
            print(f"Sistema: No hay repositorio configurado para validar '{repo_key}'.")
            return False

        # dependency_injector: llamamos al provider para obtener la instancia del repo
        # (Nota: esto crea una instancia con su sesión si es Factory, lo cual es ligero)
        repo = repo_provider()

        if repo.get_by_id(fk_id):
            return True
        else:
            print(f"Validación: No se encontró {repo_key} con ID {fk_id}.")
            return False