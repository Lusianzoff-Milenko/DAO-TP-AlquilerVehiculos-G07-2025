# controllers/vehiculo_controller.py
from typing import List, Dict, Any, Optional
from datetime import datetime
from domain.models.vehiculo import Vehiculo
from services.vehiculo_service import VehiculoService
from services.modelo_service import ModeloService
from services.color_service import ColorService


class VehiculoController:
    def __init__(self,
                 vehiculo_service: VehiculoService,
                 modelo_service: ModeloService,
                 color_service: ColorService):
        self._service = vehiculo_service
        self._modelo_service = modelo_service
        self._color_service = color_service

    def get_all_vehiculos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los vehículos y los convierte a diccionarios para la UI.
        """
        vehiculos = self._service.list_all_vehiculos()
        data = []
        for v in vehiculos:
            # Aplanamos los datos para la tabla
            data.append({
                "ID": v.id,
                "Patente": v.patente,
                "Marca": v.Modelo.Marca.nombre if (v.Modelo and v.Modelo.Marca) else "S/D",
                "Modelo": v.Modelo.nombre if v.Modelo else "S/D",
                "Color": v.Color.nombre if v.Color else "S/D",
                "Año": v.anio_fabricacion.year if v.anio_fabricacion else "S/D",
                "Precio": v.precio_base,
                "Estado": v.Estado.nombre if v.Estado else "Desconocido",
                "Chasis": v.nro_chasis
            })
        return data

    def create_vehiculo(self, data: Dict[str, Any]) -> Optional[int]:
        """
        Recibe un dict desde el formulario UI y crea el objeto Vehiculo.
        """
        try:
            # Aquí deberías buscar los IDs de modelo y color basados en la selección del combo
            # Para simplificar el ejemplo, asumo que el formulario envía IDs o que buscas por nombre
            # Nota: En una app real, el combo de la UI debería tener el ID asociado.

            nuevo_vehiculo = Vehiculo(
                patente=data.get("Patente"),
                nro_chasis=data.get("Chasis"),
                precio_base=float(data.get("Precio", 0.0)),
                # Asumiendo que data['Modelo'] es el ID del modelo seleccionado
                id_modelo=int(data.get("id_modelo")),
                id_color=int(data.get("id_color")),
                # El año puede venir como string o int
                anio_fabricacion=datetime(int(data.get("Año")), 1, 1)
            )

            return self._service.create_vehiculo(nuevo_vehiculo)
        except Exception as e:
            print(f"Error en controller creando vehículo: {e}")
            raise e

    def update_vehiculo(self, data: Dict[str, Any]) -> bool:
        try:
            v_id = data.get("ID")
            if not v_id: return False

            # Obtenemos el objeto original
            vehiculo = self._service.get_vehiculo_by_id(v_id)
            if not vehiculo: return False

            # Actualizamos campos
            vehiculo.patente = data.get("Patente")
            vehiculo.precio_base = float(data.get("Precio"))
            # Actualizar relaciones si cambiaron...

            return self._service.update_vehiculo(vehiculo)
        except Exception as e:
            print(f"Error actualizando: {e}")
            return False

    def delete_vehiculo(self, vehiculo_id: int) -> bool:
        return self._service.delete_vehiculo(vehiculo_id)

    def get_form_options(self) -> Dict[str, List]:
        """
        Retorna las listas para llenar los ComboBox del formulario (Modelos, Colores).
        """
        modelos = self._modelo_service.list_all_modelos()
        colores = self._color_service.list_all_colores()

        return {
            "modelos": [{"label": m.nombre, "value": m.id} for m in modelos],
            "colores": [{"label": c.nombre, "value": c.id} for c in colores]
        }