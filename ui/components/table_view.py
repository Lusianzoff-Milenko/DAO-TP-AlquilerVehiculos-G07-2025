"""Componente de tabla reutilizable con búsqueda y acciones."""
import dearpygui.dearpygui as dpg
from typing import Callable, List, Dict, Any, Optional

class TableView:
    """Tabla configurable con búsqueda, paginación y acciones."""
    
    def __init__(
        self,
        tag: str,
        columns: List[str],
        data: List[Dict[str, Any]] = None,
        on_row_click: Optional[Callable] = None,
        on_edit: Optional[Callable] = None,
        on_delete: Optional[Callable] = None,
        searchable: bool = True,
        page_size: int = 15
    ):
        self.tag = tag
        self.columns = columns
        self._data = data or []
        self._filtered_data = []
        self.on_row_click = on_row_click
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.searchable = searchable
        self.page_size = page_size
        self.current_page = 0
        self.selected_row = None
        
        self.container_tag = f"{tag}_container"
        self.search_tag = f"{tag}_search"
        self.table_tag = f"{tag}_table"
        self.info_tag = f"{tag}_info"
        
    def render(self, parent: str):
        """Renderiza la tabla completa."""
        with dpg.child_window(tag=self.container_tag, parent=parent, border=False):
            # Barra de búsqueda
            if self.searchable:
                with dpg.group(horizontal=True):
                    dpg.add_input_text(
                        tag=self.search_tag,
                        hint="Buscar...",
                        width=300,
                        callback=self._on_search
                    )
                    dpg.add_button(label="Buscar", callback=self._on_search)
                dpg.add_spacer(height=8)
            
            # Info de registros
            dpg.add_text("", tag=self.info_tag)
            dpg.add_spacer(height=4)
            
            # Tabla
            self._render_table()
            
            # Paginación
            dpg.add_spacer(height=8)
            self._render_pagination()
            
        self.refresh()
    
    def _render_table(self):
        """Renderiza la estructura de la tabla."""
        with dpg.table(
            tag=self.table_tag,
            header_row=True,
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
            row_background=True,
            resizable=True,
            policy=dpg.mvTable_SizingStretchProp,
            scrollY=True,
            height=400
        ):
            # Headers
            for col in self.columns:
                dpg.add_table_column(label=col)
            
            # Columna de acciones si hay callbacks
            if self.on_edit or self.on_delete:
                dpg.add_table_column(label="Acciones", width_fixed=True, init_width_or_weight=120)
    
    def _render_pagination(self):
        """Renderiza controles de paginación."""
        total_pages = max(1, (len(self._filtered_data) + self.page_size - 1) // self.page_size)
        
        with dpg.group(horizontal=True):
            dpg.add_button(
                label="< Anterior",
                callback=lambda: self._change_page(-1),
                enabled=self.current_page > 0
            )
            dpg.add_text(f"Página {self.current_page + 1} de {total_pages}")
            dpg.add_button(
                label="Siguiente >",
                callback=lambda: self._change_page(1),
                enabled=self.current_page < total_pages - 1
            )
    
    def _on_search(self):
        """Maneja la búsqueda."""
        if not self.searchable:
            return
        
        query = dpg.get_value(self.search_tag).lower().strip()
        
        if not query:
            self._filtered_data = self._data.copy()
        else:
            self._filtered_data = [
                row for row in self._data
                if any(query in str(v).lower() for v in row.values())
            ]
        
        self.current_page = 0
        self._update_table()
    
    def _change_page(self, delta: int):
        """Cambia de página."""
        self.current_page += delta
        self._update_table()
    
    def _update_table(self):
        """Actualiza el contenido de la tabla."""
        # Limpiar filas existentes
        if dpg.does_item_exist(self.table_tag):
            children = dpg.get_item_children(self.table_tag, 1)
            if children:
                for child in children:
                    dpg.delete_item(child)
        
        # Calcular rango de datos
        start_idx = self.current_page * self.page_size
        end_idx = start_idx + self.page_size
        page_data = self._filtered_data[start_idx:end_idx]
        
        # Agregar filas
        for idx, row in enumerate(page_data):
            with dpg.table_row(parent=self.table_tag):
                # Datos
                for col in self.columns:
                    value = row.get(col, "")
                    dpg.add_text(str(value))
                
                # Botones de acción
                if self.on_edit or self.on_delete:
                    with dpg.group(horizontal=True):
                        if self.on_edit:
                            dpg.add_button(
                                label="Editar",
                                callback=lambda s, a, u=row: self.on_edit(u),
                                width=60
                            )
                        if self.on_delete:
                            dpg.add_button(
                                label="Eliminar",
                                callback=lambda s, a, u=row: self.on_delete(u),
                                width=70
                            )
        
        # Actualizar info
        total = len(self._filtered_data)
        showing = len(page_data)
        dpg.set_value(self.info_tag, f"Mostrando {showing} de {total} registros")
    
    def refresh(self, new_data: Optional[List[Dict[str, Any]]] = None):
        """Refresca la tabla con nuevos datos."""
        if new_data is not None:
            self._data = new_data
        
        self._filtered_data = self._data.copy()
        self.current_page = 0
        
        if self.searchable and dpg.does_item_exist(self.search_tag):
            dpg.set_value(self.search_tag, "")
        
        self._update_table()
        
        # Actualizar paginación
        if dpg.does_item_exist(self.container_tag):
            # Re-renderizar controles de paginación
            pass
    
    def get_selected(self) -> Optional[Dict[str, Any]]:
        """Retorna la fila seleccionada."""
        return self.selected_row
    
    def clear(self):
        """Limpia todos los datos."""
        self.refresh([])
