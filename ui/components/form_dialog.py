"""Componente de diálogo modal para formularios."""
import dearpygui.dearpygui as dpg
from typing import Dict, Any, Callable, Optional, List

class FormDialog:
	"""Diálogo modal reutilizable para formularios."""
    
	def __init__(
		self,
		tag: str,
		title: str,
		fields: List[Dict[str, Any]],
		on_submit: Callable,
		on_cancel: Optional[Callable] = None,
		width: int = 500,
		height: int = 400
	):

		self.tag = tag
		self.title = title
		self.fields = fields
		self.on_submit = on_submit
		self.on_cancel = on_cancel
		self.width = width
		self.height = height
        
		self.window_tag = f"{tag}_window"
		self.error_tag = f"{tag}_error"
    
	def show(self, data: Optional[Dict[str, Any]] = None):
		"""Muestra el diálogo. Si data está presente, es modo edición."""
		if dpg.does_item_exist(self.window_tag):
			dpg.delete_item(self.window_tag)
        
		with dpg.window(
			tag=self.window_tag,
			label=self.title,
			modal=True,
			no_resize=True,
			no_move=False,
			width=self.width,
			height=self.height,
			on_close=self._on_close
		):
			# Centrar ventana
			viewport_width = dpg.get_viewport_client_width()
			viewport_height = dpg.get_viewport_client_height()
			dpg.set_item_pos(
				self.window_tag,
				[(viewport_width - self.width) // 2, (viewport_height - self.height) // 2]
			)
            
			dpg.add_spacer(height=8)
            
			# Renderizar campos en tabla de 2 columnas
			with dpg.table(header_row=False, policy=dpg.mvTable_SizingStretchProp):
				dpg.add_table_column(init_width_or_weight=0.35)
				dpg.add_table_column(init_width_or_weight=0.65)
                
				for field in self.fields:
					with dpg.table_row():
						# Label
						required_mark = " *" if field.get('required', False) else ""
						dpg.add_text(f"{field['label']}{required_mark}:")
                        
						# Input según tipo
						field_tag = f"{self.tag}_{field['key']}"
						default_value = data.get(field['key']) if data else field.get('default', '')
                        
						if field['type'] == 'text':
							dpg.add_input_text(tag=field_tag, default_value=str(default_value), width=-1)
                        
						elif field['type'] == 'number':
							dpg.add_input_int(tag=field_tag, default_value=int(default_value or 0), width=-1)
                        
						elif field['type'] == 'float':
							dpg.add_input_float(tag=field_tag, default_value=float(default_value or 0.0), width=-1)
                        
						elif field['type'] == 'combo':
							options = field.get('options', [])
							dpg.add_combo(
								tag=field_tag,
								items=options,
								default_value=str(default_value),
								width=-1
							)
                        
						elif field['type'] == 'checkbox':
							dpg.add_checkbox(tag=field_tag, default_value=bool(default_value))
                        
						elif field['type'] == 'date':
							dpg.add_input_text(
								tag=field_tag,
								default_value=str(default_value),
								hint="YYYY-MM-DD",
								width=-1
							)
			dpg.add_spacer(height=12)
            
			# Mensaje de error
			dpg.add_text("", tag=self.error_tag, color=(255, 100, 100))
            
			dpg.add_spacer(height=8)
            
			# Botones
			with dpg.group(horizontal=True):
				dpg.add_button(
					label="Guardar",
					width=120,
					callback=self._on_submit_click
				)
				dpg.add_button(
					label="Cancelar",
					width=120,
					callback=self._on_cancel_click
				)
    
	def _validate(self) -> tuple[bool, str]:
		"""Valida los campos del formulario."""
		for field in self.fields:
			if not field.get('required', False):
				continue
            
			field_tag = f"{self.tag}_{field['key']}"
			value = dpg.get_value(field_tag)
            
			if field['type'] in ['text', 'date', 'combo']:
				if not value or str(value).strip() == "":
					return False, f"El campo '{field['label']}' es requerido"
            
			elif field['type'] in ['number', 'float']:
				if value is None:
					return False, f"El campo '{field['label']}' es requerido"
        
		return True, ""
    
	def _get_form_data(self) -> Dict[str, Any]:
		"""Extrae los valores del formulario."""
		data = {}
		for field in self.fields:
			field_tag = f"{self.tag}_{field['key']}"
			data[field['key']] = dpg.get_value(field_tag)
		return data
    
	def _on_submit_click(self):
		"""Maneja el click en Guardar."""
		# Validar
		is_valid, error_msg = self._validate()
		if not is_valid:
			dpg.set_value(self.error_tag, error_msg)
			return
        
		# Limpiar error
		dpg.set_value(self.error_tag, "")
        
		# Obtener datos y llamar callback
		data = self._get_form_data()
		self.on_submit(data)
        
		# Cerrar diálogo
		self.hide()
    
	def _on_cancel_click(self):
		"""Maneja el click en Cancelar."""
		if self.on_cancel:
			self.on_cancel()
		self.hide()
    
	def _on_close(self):
		"""Maneja el cierre del diálogo."""
		if self.on_cancel:
			self.on_cancel()
    
	def hide(self):
		"""Oculta el diálogo."""
		if dpg.does_item_exist(self.window_tag):
			dpg.delete_item(self.window_tag)
