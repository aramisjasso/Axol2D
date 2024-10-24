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
                ['MAS', '+'], 
                ['COMA', ','], 
                ['MENOS', '-'], 
                ['PUNTO', '.'], 
                ['DIVISION', '/'], 
                ['DOS_PUNTOS', ':'], 
                ['PUNTO_Y_COMA', ';'], 
                ['MENOR_QUE', '<'], 
                ['MENOR_IGUAL_QUE', '<='], 
                ['IGUAL', '='], 
                ['DOBLE_IGUAL', '=='], 
                ['MAYOR_QUE', '>'], 
                ['MAYOR_IGUAL_QUE', '>='],
                ['BACKGROUND_LIBRERIA', 'Background'], 
                ['PLAYERS', 'Players'], 
                ['CORCHETE_ABRE', '['], 
                ['CORCHETE_CIERRA', ']'], 
                ['AXOL2D', 'axol2D'], 
                ['BOOLEANO', 'boolean'], 
                ['BREAK', 'break'], 
                ['BYTE', 'byte'], 
                ['CASE', 'case'], 
                ['CHAR', 'char'], 
                ['CLASS', 'class'],  
                ['DEFAULT', 'default'],  
                ['DOWHILE', 'do while'], 
                ['ELSE', 'else'], 
                ['FALSE', 'false'], 
                ['FOR', 'for'], 
                ['IF', 'if'], 
                ['IMPORT', 'import'], 
                ['INT', 'int'], 
                ['LEVEL', 'level'], 
                ['METHOD', 'method'], 
                ['MUSIC', 'music'], 
                ['NEW', 'new'], 
                ['NULL', 'null'], 
                ['OBSTACLES', 'obstacles'], 
                ['PLATFORM', 'platform'], 
                ['PLAY', 'play'], 
                ['PLAYER', 'player'], 
                ['PRINT', 'print'], 
                ['PRINT_CON', 'print_con'],
                ['RETURN', 'return'], 
                ['RIGHT', 'right'], 
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

if __name__ == '__main__':
    palabras_reservadas = [
                ['NOT', '!'], 
                ['DIFERENTE', '!='], 
                ['MODULO', '%'], 
                ['AND', '&'], 
                ['PARENTESIS_ABRE', '('], 
                ['PARENTESIS_CIERRA', ')'], 
                ['POR', '*'], 
                ['MAS', '+'], 
                ['COMA', ','], 
                ['MENOS', '-'], 
                ['PUNTO', '.'], 
                ['DIVISION', '/'], 
                ['DOS_PUNTOS', ':'], 
                ['PUNTO_Y_COMA', ';'], 
                ['MENOR_QUE', '<'], 
                ['MENOR_IGUAL_QUE', '<='], 
                ['IGUAL', '='], 
                ['DOBLE_IGUAL', '=='], 
                ['MAYOR_QUE', '>'], 
                ['MAYOR_IGUAL_QUE', '>='],
                ['BACKGROUND_LIBRERIA', 'Background'], 
                ['PLAYERS', 'Players'], 
                ['CORCHETE_ABRE', '['], 
                ['CORCHETE_CIERRA', ']'], 
                ['AXOL2D', 'axol2D'], 
                ['BOOLEANO', 'boolean'], 
                ['BREAK', 'break'], 
                ['BYTE', 'byte'], 
                ['CASE', 'case'], 
                ['CHAR', 'char'], 
                ['CLASS', 'class'],  
                ['DEFAULT', 'default'],  
                ['DOWHILE', 'dowhile'], 
                ['ELSE', 'else'], 
                ['FALSE', 'false'], 
                ['FOR', 'for'], 
                ['IF', 'if'], 
                ['IMPORT', 'import'], 
                ['INT', 'int'], 
                ['LEVEL', 'level'], 
                ['METHOD', 'method'], 
                ['OBSTACLES', 'obstacles'], 
                ['PLATFORMS', 'platforms'], 
                ['PLAY', 'play'], 
                ['PLAYER', 'player'], 
                ['PRINT', 'print'], 
                ['RETURN', 'return'], 
                ['RIGHT', 'right'], 
                ['START', 'start'], 
                ['STRING', 'string'], 
                ['SWITCH', 'switch'], 
                ['THIS', 'this'], 
                ['TRUE', 'true'], 
                ['WHILE', 'while'], 
                ['LLAVE_ABRE', '{'], 
                ['OR', '|'], 
                ['LLAVE_CIERRA', '}']]
    conatenar = []
    for x in palabras_reservadas:
        try:
            y=x[1][1]
            if x[1][1] in 'abcdefghijklmnopqrstuvwxyz':
                print(x[1])
        except IndexError:
            ''''''
        finally:
            ''''''   
        
