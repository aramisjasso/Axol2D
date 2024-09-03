from .lexico import lexer

# Funcion de prueba

def test(data):
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
           break
        print(tok)

