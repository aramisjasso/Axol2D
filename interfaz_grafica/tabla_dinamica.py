import tkinter as tk
from tkinter import ttk

class TablaDinamica:
    def __init__(self):
        self.datos = []
        
    def set_datos(self, datos):
        self.datos = datos
    
    def mostrar_tabla(self):
        # Crear una nueva ventana para la tabla
        ventana_tabla = tk.Toplevel()
        ventana_tabla.title("Tabla de Símbolos Dinámica")
        
        # Crear un widget Treeview para mostrar la tabla
        columnas = ["Lexema", "NO. ID", "Tipo de Datos", "Valor", "Declaración"]
        tree = ttk.Treeview(ventana_tabla, columns=columnas, show='headings')
        
        # Configurar encabezados de columna
        for col in columnas:
            tree.heading(col, text=col)
        
        # Insertar los datos en la tabla
        for fila in self.datos:
            tree.insert('', tk.END, values=fila)
        
        # Hacer que la tabla se ajuste al tamaño de la ventana
        tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        # Configurar el comportamiento de redimensionado
        ventana_tabla.grid_columnconfigure(0, weight=1)
        ventana_tabla.grid_rowconfigure(0, weight=1)