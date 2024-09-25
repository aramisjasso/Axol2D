import tkinter as tk
from tkinter import ttk

class TablaDinamica:
    def __init__(self):
        self.datos = []
    def set_datos (self,datos):
        self.datos = datos
    def mostrar_tabla(self):
        # Crear una nueva ventana para la tabla
        ventana_tabla = tk.Toplevel()
        ventana_tabla.title("Tabla de Simbolos Dinamica")
        
        # Crear un widget Treeview para mostrar la tabla
        columnas = ["Lexema","NO. ID","Tipo de Datos", "Valor"]
        tree = ttk.Treeview(ventana_tabla, columns=columnas, show='headings')
        # Configurar encabezados de columna
        for col in columnas:
            tree.heading(col, text=col)
        
        # Insertar los datos en la tabla
        for fila in self.datos:
            tree.insert('', tk.END, values=fila)
        
        # Mostrar el Treeview
        tree.pack(padx=10, pady=10)