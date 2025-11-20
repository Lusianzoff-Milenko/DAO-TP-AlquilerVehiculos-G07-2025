"""Componente de búsqueda con filtros."""
import dearpygui.dearpygui as dpg
from typing import Callable, Optional, List, Dict

class SearchBox:
    """Caja de búsqueda reutilizable con filtros opcionales."""
    
    def __init__(
        self,
        tag: str,
        on_search: Callable[[str, Dict], None],
        placeholder: str = "Buscar...",
        filters: Optional[List[Dict]] = None,
        width: int = 400
    ):
        """
        Args:
            tag: Identificador único
            on_search: Callback que recibe (query, filters_dict)
            placeholder: Texto de ayuda
            filters: Lista de filtros [
                {
                    'key': 'estado',
                    'label': 'Estado',
                    'type': 'combo',
                    'options': ['Todos', 'Activo', 'Inactivo']
                }
            ]
            width: Ancho del componente
        """
        self.tag = tag
        self.on_search = on_search
        self.placeholder = placeholder
        self.filters = filters or []
        self.width = width
        
        self.input_tag = f"{tag}_input"
        self.container_tag = f"{tag}_container"
    
    def render(self, parent: str):
        """Renderiza el componente de búsqueda."""
        with dpg.group(tag=self.container_tag, parent=parent, horizontal=True):
            # Input de búsqueda
            dpg.add_input_text(
                tag=self.input_tag,
                hint=self.placeholder,
                width=self.width,
                callback=lambda: self._trigger_search()
            )
            
            dpg.add_button(
                label="Buscar",
                callback=self._trigger_search
            )
            
            # Filtros adicionales
            for filter_def in self.filters:
                dpg.add_spacer(width=8)
                filter_tag = f"{self.tag}_filter_{filter_def['key']}"
                
                if filter_def['type'] == 'combo':
                    dpg.add_combo(
                        tag=filter_tag,
                        items=filter_def.get('options', []),
                        default_value=filter_def.get('options', ['Todos'])[0],
                        width=150,
                        callback=lambda: self._trigger_search()
                    )
            
            dpg.add_button(
                label="Limpiar",
                callback=self._clear_search
            )
    
    def _trigger_search(self):
        """Ejecuta la búsqueda con los valores actuales."""
        query = dpg.get_value(self.input_tag)
        
        # Recopilar valores de filtros
        filter_values = {}
        for filter_def in self.filters:
            filter_tag = f"{self.tag}_filter_{filter_def['key']}"
            filter_values[filter_def['key']] = dpg.get_value(filter_tag)
        
        self.on_search(query, filter_values)
    
    def _clear_search(self):
        """Limpia búsqueda y filtros."""
        dpg.set_value(self.input_tag, "")
        
        for filter_def in self.filters:
            filter_tag = f"{self.tag}_filter_{filter_def['key']}"
            default = filter_def.get('options', ['Todos'])[0]
            dpg.set_value(filter_tag, default)
        
        self._trigger_search()
    
    def get_query(self) -> str:
        """Obtiene el texto de búsqueda actual."""
        return dpg.get_value(self.input_tag)
    
    def get_filters(self) -> Dict[str, str]:
        """Obtiene los valores de los filtros."""
        filter_values = {}
        for filter_def in self.filters:
            filter_tag = f"{self.tag}_filter_{filter_def['key']}"
            filter_values[filter_def['key']] = dpg.get_value(filter_tag)
        return filter_values
