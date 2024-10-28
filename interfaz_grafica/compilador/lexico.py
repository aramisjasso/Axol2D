import ply.lex as lex

class Lexico():
    def __init__(self):
        #Generar lista de tokens
        self.tokens = [ 
            #Operadores Aritmeticos
            'MAS', 'MENOS', 'POR', 'DIVISION', 'MODULO', 'POTENCIA',
            #Operadores de Asignacion
            'IGUAL', 'MAS_IGUAL', 'MENOS_IGUAL', 'POR_IGUAL', 'DIVISION_IGUAL',
            #Operadores de Comparacion
            'DOBLE_IGUAL', 'DIFERENTE', 'MAYOR_QUE', 'MENOR_QUE', 'MAYOR_IGUAL_QUE', 'MENOR_IGUAL_QUE',
            #Operadores Logicos
            'AND', 'OR', 'NOT',
            #Operadores de Incremento y Decremento 
            'MAS_MAS','MENOS_MENOS',
            #Tipos de Datos
            'BOOLEANO', 'BYTE', 'INT', 'CHAR', 'STRING',
            #Delimitadores
            'PARENTESIS_ABRE', 'PARENTESIS_CIERRA', 'LLAVE_ABRE', 'LLAVE_CIERRA', 'CORCHETE_ABRE', 'CORCHETE_CIERRA', 'PUNTO', 'COMA', 'PUNTO_Y_COMA', 'DOS_PUNTOS',
            #Identificador
            'IDENTIFICADOR',
            #Número
            'NUMERO',
            #Literales y constantes
            'TRUE', 'FALSE', 'VALOR_CHAR', 'VALOR_STRING',
            # Palabras Reservadas
            'IF', 'ELSE', 'SWITCH', 'CASE', 'BREAK', 'DEFAULT', 'FOR', 'WHILE', 'DOWHILE', 'METHOD', 'RETURN',
            'START', 'PLAY', 'PRINT_CON', 'LEVEL', 'BACKGROUND', 'PLATFORM', 'OBSTACLES', 'PLAYER', 'PLAYERS',
            'AXOL2D', 'IMPORT', 'BACKGROUND_LIBRERIA','CONSTANT', 'THIS', 'NULL',
        ]

        #Palabras Reservadas
        self.palabras_reservadas = {
            # Tipos de Datos
            'boolean': 'BOOLEANO',
            'byte': 'BYTE',
            'int': 'INT',
            'char': 'CHAR',
            'string': 'STRING',
            # Estructuras de Control
            'if': 'IF',
            'else': 'ELSE',
            'switch': 'SWITCH',
            'case': 'CASE',
            'break': 'BREAK',
            'default': 'DEFAULT',
            'for': 'FOR',
            'while': 'WHILE',
            'dowhile': 'DOWHILE',
            #las demás
            'method': 'METHOD',
            'return': 'RETURN',
            'start': 'START',
            'play': 'PLAY',
            'print_con': 'PRINT_CON',
            'level': 'LEVEL',
            'background': 'BACKGROUND',
            'platform': 'PLATFORM',
            'obstacles': 'OBSTACLES',
            'player': 'PLAYER',
            'Players': 'PLAYERS',
            'axol2D': 'AXOL2D',
            'import': 'IMPORT',
            'Background': 'BACKGROUND_LIBRERIA',
            'this': 'THIS',
            'true' : 'TRUE', 
            'false' : 'FALSE'
        }
        self.errores = []

        # Inicializar el lexer
        self.lexer = lex.lex(module=self)

    #-- Operadores --
    #Operadores Aritmeticos
    t_MAS = r'\+'
    t_MENOS = r'-'
    t_POR = r'\*'
    t_DIVISION = r'/'
    t_MODULO = r'%'
    #t_POTENCIA = r'\^'

    #Operadores de Asignacion
    t_IGUAL = r'='
    # t_MAS_IGUAL = r'\+='
    # t_MENOS_IGUAL = r'-='
    # t_POR_IGUAL = r'\*='
    # t_DIVISION_IGUAL = r'/='

    # Operadores de Comparacion
    t_DOBLE_IGUAL = r'=='
    t_DIFERENTE = r'!='
    t_MAYOR_QUE = r'>'
    t_MENOR_QUE = r'<'
    t_MAYOR_IGUAL_QUE = r'>='
    t_MENOR_IGUAL_QUE = r'<='

    # Operadores Logicos
    t_AND = r'&'
    t_OR = r'\|'
    t_NOT = r'!'

    # Operadores de Incremento y Decremento
    # t_MAS_MAS = r'\+\+'
    # t_MENOS_MENOS = r'--'

    #Delimitadores
    t_PARENTESIS_ABRE = r'\('
    t_PARENTESIS_CIERRA = r'\)'
    t_LLAVE_ABRE = r'{'
    t_LLAVE_CIERRA = r'}'
    t_CORCHETE_ABRE = r'\['
    t_CORCHETE_CIERRA = r']'
    t_COMA = r','
    t_DOS_PUNTOS = r':'
    t_PUNTO_Y_COMA = r';'


    # Error número decimal no permitido en Axol2D
    def t_ERROR_LEXICO_NUMEROS_DECIMALES(self,t):
        r'( [0-9]+ \. ( (\.)* [0-9]* )* ) | (( (\.)+ [0-9]+ )+)'
        #r'([0-9]+\.[0-9]*)|([0-9]*\.[0-9]+)'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). Axol2D no permite números decimales.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        #t.lexer.skip(1)
        pass

    #Punto
    t_PUNTO = r'\.'
    
    # Error de identificador con carácter inválido
    def t_ERROR_LEXICO_4(self,t):
        r'[0-9]+ [0-9]* [a-zA-ZñÑ]+ [a-zA-Z0-9ñÑ]*'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). El identificador no es válido. Debe comenzar con una letra y puede estar seguido de dígitos o letras.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass

    def t_ERROR_LEXICO_7_6(self,t):
        r'([a-zA-Z0-9_\-\.])\''
        mensaje_error=(f"Error Léxico (Línea {t.lineno}).  Faltan comilla simple al inicio del caracter. El caracter no fue abierto.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass

    # Números int
    def t_NUMERO(self,t):
        r'[0-9]+'
        #r'(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5]?[0-9]{1,4})'
        return t

    # Valores de char y string
    def t_VALOR_CHAR(self,t):
        r"'[a-zA-ZñÑ0-9]'"
        return t

    def t_VALOR_STRING(self,t):
        r'"[a-zA-ZñÑ0-9\s_\-\.]*"'
        return t
    
    # Error de identificador largo
    def t_ERROR_LEXICO_2(self,t):
        r'[a-zA-Z] [a-zA-Z0-9]{31,}'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). El identificador  [{t.value}] supera la longitud máxima de 32 símbolos.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass

    # Identificadores
    def t_IDENTIFICADOR(self,t):
        r'[a-zA-ZñÑ]([a-zA-Z0-9ñÑ]{0,31})'
        # Verificar si es una palabra reservada
        t.type = self.palabras_reservadas.get(t.value, 'IDENTIFICADOR')

        return t
    
    

    # Regla para manejar los saltos de línea y llevar la cuenta del número de líneas
    def t_newline(self,t):
        r'\r|\n|\r\n'
        t.lexer.lineno += len(t.value)

    # Comentario de una sola línea o varias líneas
    def t_COMENTARIO(self,t):
        r'\/\/.*|/°(.|\n)*?°/'
        pass

    #Caracteres ignorados (espacios y tabulaciones)
    t_ignore = ' \t'




    def t_ERROR_LEXICO_7_5(self,t):
        r'\'([a-zA-Z0-9_\-\.])\"'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}).  Faltan comilla simple al fin del caracter. El caracter fue cerrado con comilla doble.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass


    def t_ERROR_LEXICO_7_4(self,t):
        r'\"([a-zA-Z0-9_\-\.])\''
        mensaje_error=(f"Error Léxico (Línea {t.lineno}).  Faltan comilla simple al inicio del caracter. El caracter fue abierto con comilla doble.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass
        # Error cadena no cerrada
    def t_ERROR_LEXICO_7(self,t):
        r'\"([a-zA-Z0-9_\-\.])*'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). Faltan comillas dobles al final de la cadena. La cadena no fue cerrada.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass

    # Error cadena no cerrada
    def t_ERROR_LEXICO_7_1(self,t):
        r'\"([a-zA-Z0-9_\-\.])*\''
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). Faltan comillas dobles al final de la cadena. La cadena fue cerrada con comilla simple.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass

    def t_ERROR_LEXICO_7_2(self,t):
        r'\'([a-zA-Z0-9_\-\.])*\"'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). Faltan comillas dobles al inicio de la cadena. La cadena fue abierta con comilla simple.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass

    def t_ERROR_LEXICO_7_3(self,t):
        r'\'([a-zA-Z0-9_\-\.])*\''
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). El char solo puede tener un caracter en entre sus comillas.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass
    # Error carácter no cerrado
    def t_ERROR_LEXICO_6(self,t):
        r"\'([a-zA-Z0-9_\-\.])"
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). Falta comilla simple ' a la derecha del carácter. El carácter no fue cerrado.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass







    # Error comentario no cerrado
    def t_ERROR_LEXICO_8(self,t):
        r'\/°'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). Falta '°/' para cerrar el bloque de comentarios.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass

    # Error comentario no abierto
    def t_ERROR_LEXICO_9(self,t):
        r'°\/'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). Falta '/°' al comienzo del bloque de comentarios. El comentario no fue abierto.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass

    # Error tamaño (número demasiado grande)
    # def t_ERROR_LEXICO_10(self,t):
    #     r'(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5]?[0-9]{1,4}){Digito}'
    #     mensaje_error=(f"Error Léxico (10) (Línea {t.lineno}). El número supera el máximo valor permitido en Axol2D. Solo se permiten números entre 0 y 6553.")
    #     self.errores.append([mensaje_error,t.lineno,t.lexpos])
    #     t.lexer.skip(1)

    # Error número decimal no válido
    def t_ERROR_LEXICO_11(self,t):
        r'[0-9]*("\."* [0-9]*)("\."* [0-9]*)'
        mensaje_error=(f"Error Léxico (Línea {t.lineno}). El número ingresado no es válido en el lenguaje Axol2D.")
        self.errores.append([mensaje_error,t.lineno,t.lexpos])
        pass





    # Error operador no definido en el lenguaje

    #def t_ERROR_LEXICO_5(t):
    #    r'[+\-*/%^!&|~<>]'
    #    print(f"Error Léxico (5) (Línea {t.lineno}). El operador no es válido en Axol2D.")
    #    t.lexer.skip(1)



    # Caracteres no válidos
    def t_error(self, t):
        mensaje_error = (f"Error Léxico (Línea {t.lineno}) \"{t.value[0]}\". El carácter [{t.value[0]}] no pertenece al alfabeto del lenguaje.")
        #print(mensaje_error)
        self.errores.append([mensaje_error, t.lineno, t.lexpos])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)
tokens = [
            #Operadores Aritmeticos
            'MAS', 'MENOS', 'POR', 'DIVISION', 'MODULO', 
            #Operadores de Asignacion
            'IGUAL',
            #Operadores de Comparacion
            'DOBLE_IGUAL', 'DIFERENTE', 'MAYOR_QUE', 'MENOR_QUE', 'MAYOR_IGUAL_QUE', 'MENOR_IGUAL_QUE',
            #Operadores Logicos
            'AND', 'OR', 'NOT',
            #Operadores de Incremento y Decremento 
            'MAS_MAS','MENOS_MENOS',
            #Tipos de Datos
            'BOOLEANO', 'BYTE', 'INT', 'CHAR', 'STRING',
            #Delimitadores
            'PARENTESIS_ABRE', 'PARENTESIS_CIERRA', 'LLAVE_ABRE', 'LLAVE_CIERRA', 'CORCHETE_ABRE', 'CORCHETE_CIERRA', 'PUNTO', 'COMA', 'PUNTO_Y_COMA', 'DOS_PUNTOS',
            #Identificador
            'IDENTIFICADOR',
            #Número
            'NUMERO',
            #Literales y constantes
            'TRUE', 'FALSE', 'VALOR_CHAR', 'VALOR_STRING',
            # Palabras Reservadas
            'IF', 'ELSE', 'SWITCH', 'CASE', 'BREAK', 'DEFAULT', 'FOR', 'WHILE', 'DOWHILE', 'METHOD', 'RETURN',
            'START', 'PLAY', 'PRINT_CON', 'LEVEL', 'BACKGROUND', 'PLATFORM', 'OBSTACLES', 'PLAYER', 'PLAYERS',
            'AXOL2D', 'IMPORT', 'BACKGROUND_LIBRERIA', 'THIS'
        ]