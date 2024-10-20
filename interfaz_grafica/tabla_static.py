import tkinter as tk
from tkinter import ttk

class TablaDatos:
    def __init__(self):
        self.font = ('Arial', 10)  # Define la fuente

    def mostrar_tabla(self):
        # Crear una nueva ventana para la tabla
        ventana_tabla = tk.Toplevel()
        ventana_tabla.title("Tabla de simbolos estatica")
        
        # Crear un widget Treeview para mostrar la tabla
        columnas = ["Componente Lexico", "Lexema"]
        tree = ttk.Treeview(ventana_tabla, columns=columnas, show='headings')

        # Configurar encabezados de columna
        for col in columnas:
            tree.heading(col, text=col, anchor="center")  # Centrar encabezados
            tree.column(col, anchor="center", width=150)  # Ajustar ancho de columnas

        self.palabras_reservadas = [
                ['NOT', '!'], 
                ['DIFERENTE', '!='], 
                ['MODULO', '%'], 
                ['AND', '&'], 
                ['PARENTESIS_ABRE', '('], 
                ['PARENTESIS_CIERRA', ')'], 
                ['POR', '*'], 
                ['POR_IGUAL', '*='], 
                ['MAS', '+'], 
                ['MAS_MAS', '++'], 
                ['MAS_IGUAL', '+='], 
                ['COMA', ','], 
                ['MENOS', '-'], 
                ['MENOS_MENOS', '--'], 
                ['MENOS_IGUAL', '-='], 
                ['PUNTO', '.'], 
                ['DIVISION', '/'], 
                ['DIVISION_IGUAL', '/='], 
                ['DOS_PUNTOS', ':'], 
                ['PUNTO_Y_COMA', ';'], 
                ['MENOR_QUE', '<'], 
                ['MENOR_IGUAL_QUE', '<='], 
                ['IGUAL', '='], 
                ['DOBLE_IGUAL', '=='], 
                ['MAYOR_QUE', '>'], 
                ['MAYOR_IGUAL_QUE', '>='], 
                ['CONTROLLERS', 'Controllers'], 
                ['CORCHETE_ABRE', '['], 
                ['CORCHETE_CIERRA', ']'], 
                ['POTENCIA', '^'], 
                ['AXOL2D', 'axol2D'], 
                ['BACKGROUND', 'background'], 
                ['BOOLEANO', 'boolean'], 
                ['BREAK', 'break'], 
                ['BYTE', 'byte'], 
                ['CASE', 'case'], 
                ['CHAR', 'char'], 
                ['CLASS', 'class'], 
                ['CONSTANT', 'constant'], 
                ['DEFAULT', 'default'], 
                ['DIMENSIONS', 'dimensions'], 
                ['DOWHILE', 'do while'], 
                ['DOWN', 'down'], 
                ['ELSE', 'else'], 
                ['ENEMIES', 'enemies'], 
                ['FALSE', 'false'], 
                ['FOR', 'for'], 
                ['FROM', 'from'], 
                ['GETPOSITION', 'getPosition'], 
                ['IF', 'if'], 
                ['IMPORT', 'import'], 
                ['INT', 'int'], 
                ['LEFT', 'left'], 
                ['LEVEL', 'level'], 
                ['METHOD', 'method'], 
                ['MUSIC', 'music'], 
                ['NEW', 'new'], 
                ['NULL', 'null'], 
                ['OBSTACLES', 'obstacles'], 
                ['PLATFORM', 'platform'], 
                ['PLAY', 'play'], 
                ['PLAYER', 'player'], 
                ['POSITIONX', 'positionX'], 
                ['POSITIONY', 'positionY'], 
                ['PRINT', 'print'], 
                ['PRINT_CON', 'print_con'], 
                ['RANDOM', 'random'], 
                ['READ_BIN', 'read_bin'], 
                ['READ_MG', 'read_mg'], 
                ['READ_MP3', 'read_mp3'], 
                ['READ_TEC', 'read_tec'], 
                ['RETURN', 'return'], 
                ['RIGHT', 'right'], 
                ['SAVE_BIN', 'save_bin'], 
                ['SHOW', 'show'], 
                ['START', 'start'], 
                ['STRING', 'string'], 
                ['SWITCH', 'switch'], 
                ['THIS', 'this'], 
                ['TRUE', 'true'], 
                ['UP', 'up'], 
                ['WHILE', 'while'], 
                ['LLAVE_ABRE', '{'], 
                ['OR', '|'], 
                ['LLAVE_CIERRA', '}']]

        # Insertar los datos en la tabla
        for fila in self.palabras_reservadas:
            tree.insert('', tk.END, values=fila)

        # Mostrar el Treeview
        tree.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Calcular y establecer tamaño y posición de la ventana
        screen_width = ventana_tabla.winfo_screenwidth()
        screen_height = ventana_tabla.winfo_screenheight()
        width = int(screen_width * 0.3)
        height = int(screen_height * 0.3)
        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)
        ventana_tabla.geometry(f"{width}x{height}+{x}+{y}")

