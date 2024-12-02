import tkinter as tk
from tkinter import Menu, scrolledtext, filedialog, messagebox
import clases as cs
import compilador.compilador as ts
import tabla_static as ta
import tabla_dinamica as td
import CódigoIntermedio as CI
from tkinter import font
import re



class InterfazCompilador:
    
    def __init__(self, root):
        self.root = root
        self.current_file = None #Archivo cargado
        self.text_modified = False  # Estado de modificación del texto
        # Definir fuente inicial
        self.font_size = 12
        self.font_style = font.Font(family="Monaco", size=self.font_size)
        self.menu_font = font.Font(family="Arial", size=10)
        self.setup_ui() #Inicio de GUI
        # Hacer que la ventana ocupe toda la pantalla
        self.root.state('zoomed')  # Hacer la ventana a pantalla completa
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Detecta Cierre de ventana
        self.root.bind("<Control-Shift-S>", self.guardar_archivo_como_evento)  # Detecta Ctrl + Shift + S
        # self.Código intermedio
        self.Tercetos =[]
        self.cmplr = ts.Compilador()
        self.tabla_estatica = ta.TablaDatos()
        self.tabla_dinamica_variables = td.TablaDinamica(root)
        self.tabla_dinamica_metodos = td.TablaDinamica(root, "métodos")
        self.tabla_dinamica_importaciones = td.TablaDinamica(root)
        self.CodigoIntermedio = CI.VentanaSecundaria(root,"Código Intermedio")
        self.CodigoEnsamblador = CI.VentanaSecundaria(root, "Código Ensamblador")
        #Separación de tablas
        self.variables=[]
        self.metodos=[]
        self.importaciones=[]
        
        
    def setup_ui(self):
        self.root.title("Compilador")
        
        # Menú
        menu_bar = Menu(self.root)
        
        
        # Área de texto
        self.text_area = cs.LineNumberedText(self.root)
        self.text_area.pack(fill=tk.BOTH, expand=True )
        self.root.bind("<KeyPress>", self.on_text_modified)  # Registrar cada pulsación de tecla para deshacer/rehacer más preciso
        
        self.text_area._text.config(font=self.font_style)
        self.text_area._line_numbers.config(font=self.font_style)

        # Menú
        # Archivo
        archivo_menu1 = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Archivo", menu=archivo_menu1)
        archivo_menu1.add_command(label="Nuevo (Ctrl + N)", command=self.nuevo_archivo)
        archivo_menu1.add_command(label="Abrir (Ctrl + O)", command=self.abrir_archivo)
        archivo_menu1.add_command(label="Guardar (Ctrl + S)", command=self.guardar_archivo)
        archivo_menu1.add_command(label="Guardar como (Ctrl + Shift + S)", command=self.guardar_archivo_como)
        archivo_menu1.add_separator()
        archivo_menu1.add_command(label="Salir", command=self.salir)
        
        # Edición
        archivo_menu2 = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edición", menu=archivo_menu2)
        archivo_menu2.add_command(label="Deshacer (Ctrl + Z)", command=self.text_area.deshacer) 
        archivo_menu2.add_command(label="Rehacer (Ctrl + Y)", command=self.text_area.rehacer)
        archivo_menu2.add_command(label="Cortar (Ctrl + X)", command= self.text_area.cortar)
        archivo_menu2.add_command(label="Copiar (Ctrl + C)", command= self.text_area.copiar)
        archivo_menu2.add_command(label="Pegar (Ctrl + V)", command= self.text_area.pegar)
        archivo_menu2.add_command(label="Seleccionar Todo (Ctrl + A)", command=self.text_area.seleccionar_todo)

        # Compilación
        menu_bar.add_command(label="Compilar (Ctrl + R)", command=self.compilar)

        # Tabla de simboloes
        archivo_menu3 = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tablas de Simbolos", menu=archivo_menu3)
        archivo_menu3.add_command(label="Tabla estatica ", command=self.mostrar_tabla_estatica)
        archivo_menu3.add_command(label="Tabla variables",command=self.mostrar_tabla_dinamica_variables )
        archivo_menu3.add_command(label="Tabla métodos",command=self.mostrar_tabla_dinamica_metodos )
        archivo_menu3.add_command(label="Tabla importaciones",command=self.mostrar_tabla_dinamica_importaciones )

        #Tamaño de letra
        archivo_menu4 = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Tamaño de letra", menu=archivo_menu4)
        archivo_menu4.add_command(label="Más (Ctrl + +) ", command=self.aumentar_letra())
        archivo_menu4.add_command(label="Menos (Ctrl + -)",command=self.disminuir_letra() )

        # Código Intermedio
        menu_bar.add_command(label="Código Intermedio", command=self.abrirCodigoIntermedio)

        # Código Ensamblador
        menu_bar.add_command(label="Ensamblador", command=self.abrirCodigoEnsamblador)

        self.set_menu_font(menu_bar)

        self.root.config(menu=menu_bar)

        # Consola
        self.console = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, state='disabled',font=self.font_style)
        self.console.pack(fill='x')


    #Guarda cambios del archivo
    def guardar_cambios(self):
        respuesta = messagebox.askyesnocancel(
            "Guardar cambios", 
            "¿Deseas guardar los cambios?"
        )
        if respuesta is True:
            self.guardar_archivo()
            return True
        elif respuesta is False:
            return True  # Continuar sin guardar
        else:
            return False  # Cancelar la acción
        
    #Si se cierra el archivo y no está guardado pregunta
    def on_closing(self):
        if self.text_modified:
            if not self.guardar_cambios():
                return
        self.root.destroy()
    
    #Creación de nuevo archivo
    def nuevo_archivo(self):
        if self.text_modified:
            if not self.guardar_cambios():
                return
        self.text_area.delete_text()

        self.console.config(state='normal')
        self.console.delete('1.0', tk.END)
        self.console.config(state='disabled')
        self.current_file = None
        self.text_modified = False
        self.text_area._set_checar(False)
        self.update_title()
    
    #Abrir un archivo solo .axol
    def abrir_archivo(self):
        if self.text_modified:
            if not self.guardar_cambios():
                return
             
        ruta_archivo = filedialog.askopenfilename(
            title="Selecciona un archivo", 
            filetypes=(("Archivos de AXOL2D", "*.axol"),)
        )
        
        if ruta_archivo:
            with open(ruta_archivo, 'r') as archivo:
                contenido = archivo.read()
                if contenido.endswith('\n'):
                    contenido = contenido[:-1]
                self.text_area.set_text(contenido)

                self.current_file = ruta_archivo
                self.text_modified = False
                self.text_area._set_checar(False)
                self.update_title()

    #Guarda un archivo
    def guardar_archivo(self):
        if self.current_file:
            with open(self.current_file, 'w') as archivo:
                contenido = self.text_area.get_text()
                archivo.write(contenido)
            self.text_modified = False
            self.text_area._set_checar(False)
            self.update_title()
        else:
            self.guardar_archivo_como()

    #Guarda con nombre por botones
    def guardar_archivo_como(self):
        self.guardar_archivo_como_evento(None)

    #Guarda archivo con nombre para detectar por teclado
    def guardar_archivo_como_evento(self, event):
        ruta_archivo = filedialog.asksaveasfilename(
            title="Guardar archivo como", 
            defaultextension=".axol", 
            filetypes=(("Archivos de AXOL3D", "*.axol"),)
        )
        if ruta_archivo:
            with open(ruta_archivo, 'w') as archivo:
                contenido = self.text_area.get_text()
                archivo.write(contenido)
                self.current_file = ruta_archivo
                self.text_modified = False
                self.text_area._set_checar(False)
                self.update_title()

    #Si se preciona salir pregunta si quiere guardar cambios
    def salir(self):
        if self.text_modified:
            respuesta = messagebox.askyesnocancel(
                "Salir", 
                "¿Deseas guardar los cambios antes de salir?"
            )
            if respuesta is True:
                self.guardar_archivo()
            elif respuesta is False:
                self.root.destroy()
        else:
            self.root.destroy()

    #Botón compilar
    def compilar(self):
        self.guardar_archivo()

        self.cmplr = ts.Compilador()
        self.cmplr.compilar(self.text_area.get_text())
        if self.cmplr.compilo:
            self.mostrar_resultado('Compilado de forma exitosa.')
            self.separar_tablas()
        else:
            self.mostrar_resultado(self.cmplr.errores_re())
        

    #Resultado de la compilación
    def mostrar_resultado(self, resultado):
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.insert(tk.END, f"{resultado}")
        self._color_letra_consola()
        self.console.config(state='disabled')
        

    #Detecta si se modifico el texto o se uso un shortcut
    def on_text_modified(self, event):
        if(self.text_area._text_vacio()):
            self.text_modified=False
            self.update_title()
            return
        self.text_area._on_change(event)
        if(self.text_area._get_checar()):
            self.text_modified=True
            self.update_title()
        evento = event
        self.key_pressed(evento) 
        

    #Actualiza el titulo si no están guardados los cambios
    def update_title(self):
        if self.current_file:
            if self.text_modified:
                self.root.title(f"*Compilador - {self.current_file}")
            else:
                self.root.title(f"Compilador - {self.current_file}")
        else:
            if self.text_modified:
                self.root.title("*Compilador")
            else:
                self.root.title("Compilador")

    #Detecta los shortcuts
    def key_pressed(self, event):
        if event.state == 4:  # Verificar si se presionó la tecla Control
            if event.keysym.lower() == 'n':
                self.nuevo_archivo()
                return False
            elif event.keysym.lower() == 'o':
                self.abrir_archivo()
                return False
            elif event.keysym.lower() == 's':
                self.guardar_archivo()
                return False
            elif event.keysym.lower() == 'r':
                self.compilar()
                return False
        return False
    #Tabla estatica
    def mostrar_tabla_estatica(self):
        self.tabla_estatica.mostrar_tabla()

    #Separar información de tablas:
    def separar_tablas(self):
        self.variables=[]
        self.metodos=[]
        self.importaciones=[]
        for id in self.cmplr.identificadores_ts:
            tipo =id[2]
            id_separado = id[0].split(",")
            
            if tipo in ["character","background"]:
                self.importaciones.append(id)
            elif (len(tipo) == 2 and tipo[0] == "metodo" ) or (len(id_separado)==2 and not id_separado[1].isdigit()):
                self.metodos.append(id)
            else:
                self.variables.append(id)

    #Tablas Dinanicas
    def mostrar_tabla_dinamica_variables(self):
        self.tabla_dinamica_variables.set_datos(self.variables)
        self.tabla_dinamica_variables.mostrar_tabla()
    
    def mostrar_tabla_dinamica_metodos(self):
        self.tabla_dinamica_metodos.set_datos(self.metodos)
        self.tabla_dinamica_metodos.mostrar_tabla()
    
    def mostrar_tabla_dinamica_importaciones(self):
        self.tabla_dinamica_importaciones.set_datos(self.importaciones)
        self.tabla_dinamica_importaciones.mostrar_tabla()
    #Cambiar de tamaño
    def aumentar_letra(self):
        # Aumentar el tamaño de la fuente
        self.font_size += 2
        self.font_style.configure(size=self.font_size)

    def disminuir_letra(self):
        # Disminuir el tamaño de la fuente
        if self.font_size > 2:  # Evitar un tamaño de letra menor a 2
            self.font_size -= 2
            self.font_style.configure(size=self.font_size)
    #Tamaño de menu
    def set_menu_font(self, menu):
        """Función para aplicar la fuente personalizada a todos los elementos del menú."""
        for item in menu.winfo_children():
            item.config(font=self.menu_font)
            for submenu in item.winfo_children():
               submenu.config(font=self.menu_font)

        #Color letra para la consola
    def _color_letra_consola(self):
        # Limpiar resaltado anterior
        self.console.tag_remove('resaltado', '1.0', tk.END)
        self.console.tag_remove('resaltado_linea', '1.0', tk.END)

        # Palabras clave a resaltar
        palabras_clave = ["Error Sintáctico", "Error Semántico", "Error Léxico"]

        # Obtener el texto del widget
        contenido = self.console.get("1.0", tk.END)
        
        # Resaltar palabras clave
        for palabra in palabras_clave:
            patron = fr'\b{re.escape(palabra)}\b'

            for match in re.finditer(patron, contenido):
                inicio = match.start()
                fin = match.end()
                indice_inicio = self.console.index(f"1.0 + {inicio} chars")
                indice_final = self.console.index(f"1.0 + {fin} chars")
                self.console.tag_add('resaltado', indice_inicio, indice_final)

        # Resaltar la palabra "Línea" con otro color
        patron_linea = r'\bLínea\b'
        for match in re.finditer(patron_linea, contenido):
            inicio = match.start()
            fin = match.end()
            indice_inicio = self.console.index(f"1.0 + {inicio} chars")
            indice_final = self.console.index(f"1.0 + {fin} chars")
            self.console.tag_add('resaltado_linea', indice_inicio, indice_final)

        # Configurar los estilos de las etiquetas
        self.console.tag_configure('resaltado', foreground='red')  # Color para palabras clave
        self.console.tag_configure('resaltado_linea', foreground='blue')  # Color para "Línea"

    def abrirCodigoIntermedio(self):
        Terceta = self.cmplr.codigoint.fnContatenarPilaIntermedia()
        self.CodigoIntermedio.abrir(Terceta)

    def abrirCodigoEnsamblador(self):
        Ensamblador = self.cmplr.ensamblador.codigoConvertido
        self.CodigoEnsamblador.abrir(Ensamblador)
#Inicio del main
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCompilador(root)
    root.mainloop()