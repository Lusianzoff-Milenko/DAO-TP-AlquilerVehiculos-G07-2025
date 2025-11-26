# controllers/vehiculo_controller.py
from typing import List, Dict, Any, Optional
from datetime import datetime
from domain.models.vehiculo import Vehiculo
from services.vehiculo_service import VehiculoService
from services.modelo_service import ModeloService
from services.color_service import ColorService
from services.estado_service import EstadoService
from services.marca_service import MarcaService


class VehiculoController:
    def __init__(self,
                 vehiculo_service: VehiculoService,
                 modelo_service: ModeloService,
                 color_service: ColorService,
                 estado_service: EstadoService,
                 marca_service: MarcaService):
        self._service = vehiculo_service
        self._modelo_service = modelo_service
        self._color_service = color_service
        self._estado_service = estado_service
        self._marca_service = marca_service

    def get_all_vehiculos(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los vehículos y los convierte a diccionarios para la UI.
        """
        vehiculos = self._service.list_all_vehiculos()
        data = []
        for v in vehiculos:
            # Construimos el display de Marca/Modelo
            marca_nombre = v.Modelo.Marca.nombre if (v.Modelo and v.Modelo.Marca) else "S/D"
            modelo_nombre = v.Modelo.nombre if v.Modelo else "S/D"
            marca_modelo = f"{marca_nombre} {modelo_nombre}"
            
            data.append({
                "ID": v.id,
                "Patente": v.patente,
                "Marca/Modelo": marca_modelo,
                "Color": v.Color.nombre if v.Color else "S/D",
                "Año": v.anio_fabricacion.year if v.anio_fabricacion else "S/D",
                "Estado": v.Estado.nombre if v.Estado else "Desconocido",
                "Precio Diario": f"${v.precio_base:.2f}",
                "Chasis": v.nro_chasis,
                "Precio": v.precio_base,
                # IDs para edición
                "id_modelo": v.id_modelo,
                "id_color": v.id_color,
                "id_estado": v.id_estado
            })
        return data

    def create_vehiculo(self, data: Dict[str, Any]) -> Optional[int]:
        """
        Recibe un dict desde el formulario UI y crea el objeto Vehiculo.
        """
        try:
            nuevo_vehiculo = Vehiculo(
                patente=data.get("Patente"),
                nro_chasis=data.get("Chasis"),
                precio_base=float(data.get("Precio", 0.0)),
                id_modelo=int(data.get("id_modelo")),
                id_color=int(data.get("id_color")),
                id_estado=int(data.get("id_estado", 1)),  # Default: Disponible
                anio_fabricacion=datetime(int(data.get("Año")), 1, 1)
            )

            return self._service.create_vehiculo(nuevo_vehiculo)
        except Exception as e:
            print(f"Error en controller creando vehículo: {e}")
            raise e

    def update_vehiculo(self, vehiculo_id: int, data: Dict[str, Any]) -> bool:
        """
        Actualiza un vehículo existente.
        """
        try:
            vehiculo = self._service.get_vehiculo_by_id(vehiculo_id)
            if not vehiculo:
                return False

            # Actualizar campos básicos
            vehiculo.patente = data.get("Patente")
            vehiculo.nro_chasis = data.get("Chasis")
            vehiculo.precio_base = float(data.get("Precio", 0.0))
            vehiculo.anio_fabricacion = datetime(int(data.get("Año")), 1, 1)
            
            # Actualizar relaciones
            vehiculo.id_modelo = int(data.get("id_modelo"))
            vehiculo.id_color = int(data.get("id_color"))
            vehiculo.id_estado = int(data.get("id_estado"))

            return self._service.update_vehiculo(vehiculo)
        except Exception as e:
            print(f"Error actualizando vehículo: {e}")
            return False

    def delete_vehiculo(self, vehiculo_id: int) -> bool:
        try:
            return self._service.delete_vehiculo(vehiculo_id)
        except Exception as e:
            print(f"Error eliminando vehículo: {e}")
            return False

    def get_form_options(self) -> Dict[str, List]:
        """
        Retorna las listas para llenar los ComboBox del formulario.
        """
        modelos = self._modelo_service.list_all_modelos()
        colores = self._color_service.list_all_colores()
        estados = self._estado_service.get_estado_by_ambito("vehiculo")

        return {
            "modelos": [{"label": f"{m.Marca.nombre} {m.nombre}" if m.Marca else m.nombre, "value": m.id} for m in modelos],
            "colores": [{"label": c.nombre, "value": c.id} for c in colores],
            "estados": [{"label": e.nombre, "value": e.id} for e in estados]
        }