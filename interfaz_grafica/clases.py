import tkinter as tk
import re

class LineNumberedText(tk.Frame):
    checar = False
    
    def __init__(self, *args, **kwargs,):
        tk.Frame.__init__(self, *args, **kwargs)
        self.numero_lineas = 0
        self._line_numbers = tk.Text(self, width=4, padx=5, takefocus=0, border=0,
                                     background='lightgrey', state='disabled')
        self._line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Crear una barra de desplazamiento
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Caja de texto
        self._text = tk.Text(self, wrap='word', undo=True, autoseparators=False, yscrollcommand=self._on_scroll)
        self._text.configure(tabs=('1c'))
        self._text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        # Configurar la barra de desplazamiento para que controle el widget de texto
        self.scrollbar.config(command=self._yview)

        # Crear la etiqueta "resaltado" y configurar el color de texto
        self._text.tag_config('resaltado', foreground='blue')

        # Evento que se activa al escribir en el Texto
        self._text.bind('<Key>', self._add_separator)  # Add this line

        # Revisar el hacer y el des hacer
        self._text.bind('<Control-z>', self.deshacer)
        self._text.bind('<Control-y>', self.rehacer)


    #Para checar cada  cambio en el documento
    def _on_change(self, event=None):
        num_lines = int(self._text.index('end-1c').split('.')[0])
        if num_lines!= self.numero_lineas:
            self.numero_lineas=num_lines
            self._update_line_numbers()
        tecla = event
        if event.state == 4:
            self.checar = self.key_pressed(tecla)
            return 

        tecla = event.keysym
        if tecla not in ['Shift_L', 'Shift_R', 'Control_L', 'Control_R', 'Alt_L', 'Alt_R',
                         'Caps_Lock', 'Escape', 'Fn', 'Left', 'Right', 'Up', 'Down', 
                         'Page_Up', 'Page_Down', 'Home', 'End', 'F1', 'F2', 'F3', 'F4', 
                         'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'Insert','XF86AudioMute',
                         'XF86AudioLowerVolume', 'XF86AudioRaiseVolume', 'Win_L', '??']:
            self.checar = True  # Regresa true
            #self._color_letra()
            return
        self.checar = False

    #Texto vacio
    def _text_vacio (self):
        cadena= self.get_text()
        if(cadena == "\n"):
            return True

    #Cambia el color si se modifico
    # def _color_letra(self):
    #     # Limpiar resaltado anterior
    #     self._text.tag_remove('resaltado', '1.0', tk.END)

    #     # Palabras clave a resaltar
    #     palabras_clave = ["Python", "Tkinter", "color"]

    #     # Obtener el texto del widget
    #     contenido = self._text.get("1.0", tk.END)
        
    #     # Iterar sobre cada palabra clave
    #     for palabra in palabras_clave:
    #         # Crear una expresión regular que busque la palabra exacta
    #         # Asegurando que la palabra esté separada por un delimitador como espacio, inicio o fin de línea
    #         patron = fr'\b{re.escape(palabra)}\b'

    #         # Buscar todas las ocurrencias de la palabra clave en el texto
    #         for match in re.finditer(patron, contenido):
    #             # Calcular las posiciones inicial y final de la coincidencia
    #             inicio = match.start()
    #             fin = match.end()

    #             # Convertir las posiciones a índices compatibles con Tkinter
    #             indice_inicio = f"1.0 + {inicio}c"
    #             indice_final = f"1.0 + {fin}c"

    #             # Aplicar la etiqueta "resaltado" al texto encontrado
    #             self._text.tag_add('resaltado', indice_inicio, indice_final)    
    


    #checar si el código de modifico y se guardo
    def _get_checar(self):
        return self.checar
    def _set_checar(self, recibir):
        self.checar = recibir

    #Actualizar el número de linea
    def _update_line_numbers(self):
        line_numbers = "\n".join(map(str, range(1, int(self._text.index('end-1c').split('.')[0]) + 1)))
        self._line_numbers.config(state=tk.NORMAL)
        self._line_numbers.delete(1.0, tk.END)
        self._line_numbers.insert(1.0, line_numbers)
        self._line_numbers.config(state=tk.DISABLED)

    #Separador de control "x" y "y" 
    def _add_separator(self, event):
        self._text.edit_separator()  # Add undo separator
    
    #Ver el movimiento de la barra lateral
    def _yview(self, *args):
        self._text.yview(*args)
        self._line_numbers.yview(*args)

    #Movimiento de scroll
    def _on_scroll(self, *args):
        self.scrollbar.set(*args)
        self._line_numbers.yview_moveto(args[0])
        
    def get_text_widget(self):
        return self._text
    
    #Optener texto  
    def get_text(self):
        return self._text.get("1.0", tk.END)
    
    #Poner Texto
    def set_text(self, contenido):
        self._text.delete(1.0, tk.END)
        self._text.insert(tk.END, contenido)
        self._text.edit_reset()
        self._update_line_numbers()
    
    #Borrar Texto
    def delete_text(self):
        self._text.delete(1.0, tk.END)

    #Método para detectar shorts keys
    def key_pressed(self, event):
        if event.state == 4:  # Verificar si se presionó la tecla Control
            if event.keysym.lower() == 'n':
                return False
            elif event.keysym.lower() == 'o':
                return False
            elif event.keysym.lower() == 's':
                return False
            elif event.keysym.lower() == 'x':
                return True
            elif event.keysym.lower() == 'c':
                return False
            elif event.keysym.lower() == 'v':
                return True
            elif event.keysym.lower() == 'a':
                return False
            elif event.keysym.lower() == 'r':
                return False
        return False
    
    def deshacer(self, event=None):
        try:
            self._text.edit_undo()
            return 'break'
        except tk.TclError:
            pass
#----------------------------------- Funciones de escritura ------------------------------------
    # Rehace lo escrito
    def rehacer(self, event=None):
        try:
            self._text.edit_redo()
            return 'break'
        except tk.TclError:
            pass

    #Corta por botón
    def cortar(self):
        self._text.event_generate("<<Cut>>")

    #Copia por botón
    def copiar(self):
        self._text.event_generate("<<Copy>>")

    #Pega por botón
    def pegar(self):
        self._text.event_generate("<<Paste>>")

    #Función para seleccionar todo lo escrito
    def seleccionar_todo(self):
        self._text.tag_add("sel", "1.0", "end")
        self._text.mark_set("insert", "1.0")
        self._text.mark_set("end", "end")

