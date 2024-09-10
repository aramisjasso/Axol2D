import compilador.Lexico as lexico

# Clase del compilador
class Compilador():
    def __init__(self):
        self.lexi = lexico.Lexico()
        self.tokens = []#Lista de tokens
        self.identificadores = [] #Lista de identificadores
        self.identificadores_ts = []
        self.errores_lexicos = []#Lista de errores lexicos
        self.compilo = True #Si compilo

    #Parte_del lexico
    def parte_Lexico(self,data):
        self.tokens = [] #Reinicia la lista de tokens
        self.errores_lexicos = []
        self.identificadores=[]

        self.lexi.lexer.lineno = 1 #Reincia el número de linea
        self.lexi.lexer.input(data) #Se pasa la información
        self.compilo = True #Si todo compilo bien
        while True:
            tok = self.lexi.lexer.token()
            if not tok:
                self.compilo=False
                break
            self.tokens.append(tok)
            if tok.type == 'IDENTIFICADOR': #Agrega a la lista de identificadores
                    self.revisar_ts(tok)
            print(tok)
        self.errores_lexicos=self.lexi.errores
        self.identificadores_lista()
    #Errores
    def errores(self):
        mensajes=''
        for error in self.errores_lexicos:
            mensajes+=(error[0])
        return mensajes
    
    #Revisa la lista de identificadores, agrega el token y los ordena
    def revisar_ts(self,tok):
        for token in self.identificadores:
            if token.value == tok.value :
                return 
        self.identificadores.append(tok)
        self.identificadores = sorted(self.identificadores, key=lambda x: x.value)
                

    def identificadores_lista(self):
        self.identificadores_ts=[]
        for token in self.identificadores:
            self.identificadores_ts.append([token.value,'Sin tipo', 'Sin Valor'])
        return self.identificadores_ts
            