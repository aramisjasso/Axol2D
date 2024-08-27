import ply.lex as lex

#Generar lista de tokens
tokens = [ 
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
    'START', 'SHOW', 'PRINT', 'READ_TEC', 'READ_BIN', 'READ_MP3', 'READ_MG', 'SAVE_BIN', 'GETPOSITION', 'RANDOM',
    'PLAY', 'PRINT_CON', 'LEVEL', 'DIMENSIONS', 'BACKGROUND', 'PLATFORM', 'OBSTACLES', 'PLAYER', 'ENEMIES', 'MUSIC',
    'AXOL2D', 'POSITIONY', 'POSITIONX', 'IMPORT', 'CLASS', 'FROM', 'NEW', 'CONTROLLERS', 'UP', 'DOWN', 'LEFT', 'RIGHT',
    'CONSTANT', 'THIS', 'NULL',
]

#Palabras Reservadas
palabras_reservadas = {
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
    'do while': 'DOWHILE',
    #las demás
    'method': 'METHOD',
    'return': 'RETURN',
    'start': 'START',
    'show': 'SHOW',
    'print': 'PRINT',
    'read_tec': 'READ_TEC',
    'read_bin': 'READ_BIN',
    'read_mp3': 'READ_MP3',
    'read_mg': 'READ_MG',
    'save_bin': 'SAVE_BIN',
    'getPosition': 'GETPOSITION',
    'random': 'RANDOM',
    'play': 'PLAY',
    'print_con': 'PRINT_CON',
    'level': 'LEVEL',
    'dimensions': 'DIMENSIONS',
    'background': 'BACKGROUND',
    'platform': 'PLATFORM',
    'obstacles': 'OBSTACLES',
    'player': 'PLAYER',
    'enemies': 'ENEMIES',
    'music': 'MUSIC',
    'axol2D': 'AXOL2D',
    'positionY': 'POSITIONY',
    'positionX': 'POSITIONX',
    'import': 'IMPORT',
    'class': 'CLASS',
    'from': 'FROM',
    'new': 'NEW',
    'Controllers': 'CONTROLLERS',
    'up': 'UP',
    'down': 'DOWN',
    'left': 'LEFT',
    'right': 'RIGHT',
    'constant': 'CONSTANT',
    'this': 'THIS',
    'null': 'NULL',
    'true': 'TRUE',
    'false': 'FALSE'
}

#-- Operadores --
#Operadores Aritmeticos
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIVISION = r'/'
t_MODULO = r'%'
t_POTENCIA = r'\^'

#Operadores de Asignacion
t_IGUAL = r'='
t_MAS_IGUAL = r'\+='
t_MENOS_IGUAL = r'-='
t_POR_IGUAL = r'\*='
t_DIVISION_IGUAL = r'/='

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
t_MAS_MAS = r'\+\+'
t_MENOS_MENOS = r'--'

#Delimitadores
t_PARENTESIS_ABRE = r'\('
t_PARENTESIS_CIERRA = r'\)'
t_LLAVE_ABRE = r'{'
t_LLAVE_CIERRA = r'}'
t_CORCHETE_ABRE = r'\['
t_CORCHETE_CIERRA = r']'
t_PUNTO = r'\.'
t_COMA = r','
t_PUNTO_Y_COMA = r';'
t_DOS_PUNTOS = r':'

# Números int
def t_NUMERO(t):
    r'(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5]?[0-9]{1,4})'
    return t

# Valores booleanos
t_TRUE = r'true'
t_FALSE = r'false'

# Valores de char y string
def t_VALOR_CHAR(t):
    r"'[a-zA-Z0-9\s]'"
    return t

def t_VALOR_STRING(t):
    r'"[a-zA-Z0-9\s_\-\.]*"'
    return t

# Identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z]([a-zA-Z0-9]{0,31})'
    # Verificar si es una palabra reservada
    t.type = palabras_reservadas.get(t.value, 'IDENTIFICADOR')

    return t

# Regla para manejar los saltos de línea y llevar la cuenta del número de líneas
def t_newline(t):
    r'\r|\n|\r\n'
    t.lexer.lineno += len(t.value)

# Comentario de una sola línea o varias líneas
def t_COMENTARIO(t):
    r'\/\/.*|/°(.|\n)*?°/'
    pass

#Caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

# Error cadena no cerrada
def t_ERROR_LEXICO_7(t):
    r'\"([a-zA-Z0-9_\-\.])*'
    print(f"Error Léxico (7) en la línea {t.lineno}. Faltan comillas dobles al final de la cadena. La cadena no fue cerrada.")
    t.lexer.skip(1)

# Error comentario no cerrado
def t_ERROR_LEXICO_8(t):
    r'\/°'
    print(f"Error Léxico (8) en la línea {t.lineno}. Falta '°/' para cerrar el bloque de comentarios.")
    t.lexer.skip(1)

# Error comentario no abierto
def t_ERROR_LEXICO_9(t):
    r'°\/'
    print(f"Error Léxico (9) en la línea {t.lineno}. Falta '/°' al comienzo del bloque de comentarios. El comentario no fue abierto.")
    t.lexer.skip(1)

# Error tamaño (número demasiado grande)
def t_ERROR_LEXICO_10(t):
    r'(6553[0-5]|655[0-2][0-9]|65[0-4][0-9]{2}|6[0-4][0-9]{3}|[1-5]?[0-9]{1,4}){Digito}'
    print(f"Error Léxico (10) en la línea {t.lineno}. El número supera el máximo valor permitido en Axol2D. Solo se permiten números entre 0 y 6553.")
    t.lexer.skip(1)

# Error número decimal no válido
def t_ERROR_LEXICO_11(t):
    r'[0-9]*("\."* [0-9]*)("\."* [0-9]*)'
    print(f"Error Léxico (11) en la línea {t.lineno}. El número ingresado no es válido en el lenguaje Axol2D.")
    t.lexer.skip(1)

# Error número decimal no permitido en Axol2D
def t_ERROR_LEXICO_3(t):
    r'[0-9]*\.[0-9]*'
    print(f"Error Léxico (3) en la línea {t.lineno}. Axol2D no permite números decimales.")
    t.lexer.skip(1)

# Error de identificador largo
def t_ERROR_LEXICO_2(t):
    r'[a-zA-Z]([a-zA-Z0-9])*'
    if len(t.value) > 32:
        print(f"Error Léxico (2) en la línea {t.lineno}. El identificador supera la longitud máxima de 32 símbolos.")
        t.lexer.skip(1)

# Error de identificador con carácter inválido
def t_ERROR_LEXICO_4(t):
    r'[a-zA-Z][^a-zA-Z0-9_]'
    print(f"Error Léxico (4) en la línea {t.lineno}. El identificador no es válido. Debe comenzar con una letra y puede estar seguido de dígitos o letras.")
    t.lexer.skip(1)

# Error operador no definido en el lenguaje
def t_ERROR_LEXICO_5(t):
    r'[+\-*/%^!&|~<>]'
    print(f"Error Léxico (5) en la línea {t.lineno}. El operador no es válido en Axol2D.")
    t.lexer.skip(1)

# Error carácter no cerrado
def t_ERROR_LEXICO_6(t):
    r"\'([a-zA-Z0-9_\-\.])"
    print(f"Error Léxico (6) en la línea {t.lineno}. Falta comilla simple ' a la derecha del carácter. El carácter no fue cerrado.")
    t.lexer.skip(1)

# Caracteres no válidos
def t_ERROR_LEXICO_1(t):
    r'[^a-zA-Z0-9_\-\.]'
    print(f"Error Léxico (1) en la línea {t.lineno}. El identificador no es válido. Debe comenzar con una letra y puede estar seguido de dígitos o letras.")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Funcion de prueba
def test(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(tok)

# Prueba del lexer
if __name__ == "__main__":
    data = '''
        import Controllers;
    import DesignElements from DesignAxol2D;
    import libreria from ubicacion;

    level MiPrimerNivel  {

        int a;    
        int i = 0 ;
        string cadena = "mi primer cadena";
        boolean bandera = true;
        char c = 'a'; //Error
        int [2] arreglo;
        enemies[2] enemigos;
        int[5] miArreglo = [1, 2, 3, 4, 5];
        int[2][2] matriz2 = [[1, 2], [3, 4]]; 
        enemies[2] enemigos;
        int[5][8] dotMatrix;
        dimensions dm = [1000,  200]; // x , y 200 - 20000    
        background bg = "fondoCastilloBowser.jpg"; //Color o imagen debe de
    // medir lo mismo
        platform pt = Platforms.LavaCastle; //Plataforma en forma de castillo de lava
        backElement portalFinal = "portal.png "; //Imagen de un portal como parte de elemento del fondo principal
        obstacles obs = block[100] ; //Creacion de 100 bloques 
        player py = Players.Mario; // atributo extendido de controllers
        begin b = [5,0]; // donde inicia el personaje extendido de controllers
        finish f = [990,0]; // finalización del nivel en la posición
        lifes life = [100,3]; // cantidad de vidas y cuanta vida tiene cada una
        
        enemies[2] en = [Enemies.Goomba, Enemies.KoopaTropa]; //Se pasa los enemigos
        music ms = "Musica de fondo.mp3";

        method boolean design(int a, byte c) {
            //Posicionamiento de bloques
            obs.positionY(0);
            obs.positionX(100); 
            //elemento de imagen importado
            portalFinal.position(990,0);
            bg.add(portalFinal);	
            en[0].set(10, "Basico");
            en[0].position(200); 
            en[0].getPosition();
            en[1].set(5);
            en[1].position(700);
            puntaje = -b*(b^2-4*a*c)/2;
            if( x < y ){
            en[0].getPosition();
            }
        
            return true;
        }


        method boolean miPrimerMetodo (int a, int b, int c, string d) {
            m2 = m2.set(3, 4);
            m3 = miMetodo(1 + 1, 3);
            
            return true;
        }

        method boolean miPrimerMetodo (int a, int b, int c, string d) {
            m2 = m2.set(3, 4);
            m3 = miMetodo(1 + 1, 3);

            if (i > 0) {
                i = i + 1; 
                a = new Clase();
            } else {
                m3 = miMetodo(1 + 1, 3);  
                if (i > 0) {
                    i = i + 1; 
                    a  = new Clase();
                }
            }

            switch (hola) {
                case hola > 0 :
                    i = i + 1; 
                    break;
                case hola > 0 :
                    i = i + 1; 
                    break;
                case hola > 0 :
                    i = i + 1; 
                    break;
                default :
                    i = i + 1; 
            }

            for (int h = 1; h > 10; i = i + 1) {
                i = i + 1; 
                if (i > 0) {
                    i = i + 1; 
                    a = new Clase();
                }
            }

            while (1 < a) {
                i = i + 1; 
            }

            do while (1 < a) {
                i = i + 1;
                if (i > 0) {
                    i = i + 1; 
                    a = new Clase();
                }
            }

            return true;
        }

        axol2D play() {
            // Contenido del método play
            MiPrimerNivel.start();
        }

    }
    '''
    test(data)

