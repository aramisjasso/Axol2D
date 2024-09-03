import tkinter as tk
from tkinter import Menu, scrolledtext, filedialog, messagebox
import clases as cs
import compilador.compilador as ts



class InterfazCompilador:
    
    def __init__(self, root):
        self.root = root
        self.current_file = None #Archivo cargado
        self.text_modified = False  # Estado de modificación del texto
        self.setup_ui() #Inicio de GUI
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Detecta Cierre de ventana
        self.root.bind("<Control-Shift-S>", self.guardar_archivo_como_evento)  # Detecta Ctrl + Shift + S
        

    def setup_ui(self):
        self.root.title("Compilador")
        
        # Menú
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # Área de texto
        self.text_area = cs.LineNumberedText(self.root)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.root.bind("<KeyPress>", self.on_text_modified)  # Registrar cada pulsación de tecla para deshacer/rehacer más preciso
        
        

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
        archivo_menu3.add_command(label="Tabla estatica", ) 
        archivo_menu3.add_command(label="Tabla dinamica", )



        # Consola
        self.console = scrolledtext.ScrolledText(self.root, height=10, wrap=tk.WORD, state='disabled')
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
        resultado = ts.test(self.text_area.get_text())
        self.mostrar_resultado('Todo salio bien')

    #Resultado de la compilación
    def mostrar_resultado(self, resultado):
        self.console.config(state='normal')
        self.console.insert(tk.END, resultado + '\n')
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
    



#Inicio del main
if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCompilador(root)
    root.mainloop()