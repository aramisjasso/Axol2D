import ply.lex as lex
import ply.yacc as yacc

# Definición de tokens y lexer
tokens = ['NUMBER', 'PLUS', 'MINUS']

t_PLUS = r'\+'
t_MINUS = r'-'
t_NUMBER = r'\d+'

def t_error(t):
    # Agregar el error léxico a la lista de errores de la clase
    error_message = f"Error léxico en la línea {t.lineno}: Carácter ilegal '{t.value[0]}'"
    lexer.compilador.errores.append(error_message)
    t.lexer.skip(1)

lexer = lex.lex()

# Reglas de gramática
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_term_number(p):
    'term : NUMBER'
    p[0] = int(p[1])

# Manejo de errores de sintaxis
def p_error(p):
    if p:
        error_message = f"Error de sintaxis en la línea {p.lineno}: Token inesperado '{p.value}'"
        lexer.compilador.errores.append(error_message)
    else:
        error_message = "Error de sintaxis: Fin de entrada inesperado"
        lexer.compilador.errores.append(error_message)

# Construcción del parser
parser = yacc.yacc()

# Clase Compilador
class Compilador:
    def __init__(self):
        self.tokens = []   # Lista para almacenar tokens válidos
        self.errores = []  # Lista para almacenar errores léxicos y sintácticos

    def test(self, data):
        self.tokens = []   # Reiniciar la lista de tokens
        self.errores = []  # Reiniciar la lista de errores
        lexer.lineno = 1   # Reiniciar el número de línea
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok:
                break
            self.tokens.append(tok)  # Agregar el token válido a la lista
        # Ejecutar el parser
        parser.parse(data, lexer=lexer)

# Crear una instancia de Compilador
mi_compilador = Compilador()

# Asociar la instancia del compilador al lexer
lexer.compilador = mi_compilador

# Ejecutar la prueba
mi_compilador.test('3 + 4 - 5 *')

# Acceder a los tokens y errores
print("Tokens:", mi_compilador.tokens)
print("Errores:", mi_compilador.errores)
