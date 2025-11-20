"""Componente de tarjeta KPI para dashboard."""
import dearpygui.dearpygui as dpg
from typing import Optional, Tuple

class KPICard:
    """Tarjeta de métrica/KPI reutilizable."""
    
    def __init__(
        self,
        tag: str,
        title: str,
        value: str = "0",
        subtitle: str = "",
        color: Optional[Tuple[int, int, int, int]] = None,
        icon: str = "[KPI]"
    ):
        """
        Args:
            tag: Identificador único
            title: Título de la métrica
            value: Valor principal
            subtitle: Descripción o tendencia
            color: Color del borde/acento (R, G, B, A)
            icon: Emoji o símbolo
        """
        self.tag = tag
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.color = color or (56, 117, 215, 255)
        self.icon = icon
        
        self.container_tag = f"{tag}_container"
        self.value_tag = f"{tag}_value"
        self.subtitle_tag = f"{tag}_subtitle"
    
    def render(self, parent: str, width: int = 220, height: int = 120):
        """Renderiza la tarjeta KPI."""
        with dpg.child_window(
            tag=self.container_tag,
            parent=parent,
            width=width,
            height=height,
            border=True
        ):
            dpg.add_spacer(height=8)
            
            # Icono y título
            with dpg.group(horizontal=True):
                dpg.add_text(self.icon)
                dpg.add_text(self.title, color=(200, 200, 200))
            
            dpg.add_spacer(height=6)
            
            # Valor principal (grande)
            dpg.add_text(
                self.value,
                tag=self.value_tag,
                color=self.color
            )
            
            dpg.add_spacer(height=4)
            
            # Subtítulo
            dpg.add_text(
                self.subtitle,
                tag=self.subtitle_tag,
                color=(150, 150, 150)
            )
    
    def update(self, value: str, subtitle: Optional[str] = None):
        """Actualiza los valores de la tarjeta."""
        if dpg.does_item_exist(self.value_tag):
            dpg.set_value(self.value_tag, value)
        
        if subtitle is not None and dpg.does_item_exist(self.subtitle_tag):
            dpg.set_value(self.subtitle_tag, subtitle)
    
    def set_color(self, color: Tuple[int, int, int, int]):
        """Cambia el color del valor."""
        self.color = color
        if dpg.does_item_exist(self.value_tag):
            dpg.configure_item(self.value_tag, color=color)
