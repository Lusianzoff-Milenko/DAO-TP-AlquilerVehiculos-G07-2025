from typing import Dict, Any

class ValidationMapper:
    """
    Clase para centralizar la validación de existencia de IDs (Foreign Keys)
    utilizando una colección de repositorios inyectados.
    """
    def __init__(self, repositories: Dict[str, Any]):
        """
        Inicializa con un diccionario de repositorios (e.g., {'marca': MarcaRepository}).
        """
        self._repos = repositories

    def validate_fk_exists(self, repo_key: str, fk_id: int, fk_name: str) -> bool:
        """
        Verifica si un ID de clave foránea existe en su repositorio asociado.

        :param repo_key: Clave del repositorio en el diccionario (e.g., 'marca').
        :param fk_id: El ID a buscar.
        :param fk_name: Nombre del campo (para el mensaje de error).
        :return: True si existe, False si no existe o el repositorio no está disponible.
        """
        if fk_id is None or fk_id <= 0:
            print(f"Validation Error: {fk_name} debe ser un ID positivo.")
            return False

        repo = self._repos.get(repo_key)
        if not repo:
            print(f"System Error: Repositorio '{repo_key}' no disponible para validación.")
            return False

        if repo.get_by_id(fk_id):
            return True
        else:
            print(f"Validation Error: ID '{fk_id}' para {fk_name} no existe en la base de datos.")
            return False