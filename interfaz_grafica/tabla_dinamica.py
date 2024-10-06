import tkinter as tk
from tkinter import ttk

class TablaDinamica:
    def __init__(self, root):
        self.datos = []
        self.root = root
    
    def set_datos(self, datos):
        self.datos = datos
    
    def mostrar_tabla(self):
        # Crear una nueva ventana para la tabla
        ventana_tabla = tk.Toplevel(self.root)
        ventana_tabla.title("Tabla de Símbolos Dinámica")
        
        # Crear un widget Treeview para mostrar la tabla
        columnas = ["Lexema", "NO. ID", "Tipo de Datos", "Valor", "Declaración"]
        tree = ttk.Treeview(ventana_tabla, columns=columnas, show='headings')
        
        # Configurar encabezados de columna
        for col in columnas:
            tree.heading(col, text=col)
        #Datos sin comas
        datos=self.fnFilasTodas()

        # Insertar los datos en la tabla
        for fila in datos:
            tree.insert('', tk.END, values=fila)
        
        # Hacer que la tabla se ajuste al tamaño de la ventana
        tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        # Configurar el comportamiento de redimensionado
        ventana_tabla.grid_columnconfigure(0, weight=1)
        ventana_tabla.grid_rowconfigure(0, weight=1)
        
        # Vincular el evento de selección de fila
        tree.bind("<<TreeviewSelect>>", self.on_row_select)
    
    def on_row_select(self, event):
        # Obtener la fila seleccionada
        tree = event.widget
        selected_item = tree.selection()[0]
        valores_fila = tree.item(selected_item, "values")
        print(valores_fila)
        ar='arreglo'
        ma='matriz'
        me='metodo'
        temp_id=valores_fila[0]
        if  ar in valores_fila[2]:
            self.ventana(temp_id,ar)
        elif 'matriz'in valores_fila[2]:
            self.ventana(temp_id, ma)
        elif 'metodo' in valores_fila[2]:
            self.ventana(temp_id, me)
        
    def ventana(self,id, tipo):
            indice=self.fnIndice(id)
            # Crear una nueva ventana con los detalles del elemento seleccionado
            ventana_detalle = tk.Toplevel(self.root)
            ventana_detalle.title(f"Detalles de {tipo} el identificador \"{id}\"")
            
            # Mostrar los detalles del elemento en la nueva ventana
            texto=''
            for idx, col in enumerate(["Lexema", "NO. ID", "Tipo de Datos", "Elementos", "Declaración"]):
                texto+=f"{col}: {self.datos[indice][idx]}\t"
            etiqueta = tk.Label(ventana_detalle, text=texto)

            columnas = ["Lexema", "NO. ID", "Tipo de Datos", "Valor", "Declaración"]
            tree = ttk.Treeview(ventana_detalle, columns=columnas, show='headings')
            
            # Configurar encabezados de columna
            for col in columnas:
                tree.heading(col, text=col)
            temp_fila=self.fnFilasVentana(id)
            # Insertar los datos en la tabla
            if len(temp_fila)!=0:
                for fila in temp_fila:
                    tree.insert('', tk.END, values=fila)
                    etiqueta.pack(padx=10, pady=5)

                    # Hacer que la tabla se ajuste al tamaño de la ventana
            tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    def fnFilasTodas(self):
        lista=[]
        for indice, simbolo in enumerate(self.datos):
            temp_id=simbolo[0]
            if  not ',' in temp_id:
                lista.append(simbolo)
        return lista
#---------------------------------------------------------------------------------
    def fnFilasVentana(self,id):
        lista=[]
        for indice, simbolo in enumerate(self.datos):

            temp_id=simbolo[0]
            lista_id= temp_id.split(",")
            if id==lista_id[0] and id!=temp_id:
                lista.append(simbolo)
        return lista
#---------------------------------------------------------------------------------
    def fnIndice(self,id):
        simbolo = None
        for indice, simbolo in enumerate(self.datos):
            if simbolo[0] == id:
                simbolo=indice
                break
        return simbolo
