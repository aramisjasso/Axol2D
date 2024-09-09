import compilador.Lexico as lexico

# Clase del compilador
class Compilador():
    def __init__(self):
        self.lexi = lexico.Lexico()
        self.tokens = []#Lista de tokens
        self.errores_lexicos = []#Lista de errores lexicos
        self.compilo = True #Si compilo

    #Parte_del lexico
    def parte_Lexico(self,data):
        self.tokens = [] #Reinicia la lista de tokens
        self.lexi.lexer.lineno = 1 #Reincia el número de linea
        self.lexi.lexer.input(data) #Se pasa la información
        self.compilo = True
        while True:
            tok = self.lexi.lexer.token()
            if not tok:
                self.compilo=False
                break
            self.tokens.append(tok)
            print(tok)
        self.errores_lexicos=self.lexi.errores

    def errores(self):
        mensajes=''
        for error in self.errores_lexicos:
            mensajes+=(error[0])
        return mensajes


