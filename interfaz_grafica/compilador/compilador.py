import compilador.lexico as lexico
import compilador.sintactico as sintactico

# Clase del compilador
class Compilador():
    def __init__(self):
        self.lexi = lexico.Lexico() #Lexico
        self.sin = sintactico.Sintactico()
        self.tokens = []#Lista de tokens
        self.identificadores = [] #Lista de identificadores
        self.identificadores_ts = []
        self.errores_lexicos = []#Lista de errores lexicos
        self.errores_sintacticos = [] #Lista de errores Sintacticos
        self.errores_lista = [] #Lista de todos los errores
        self.compilo = True #Si compilo
        self.varId = 0

    def compilar(self,data):
        self.parte_Lexico(data)
        self.parte_Sintactica(data,self.lexi.lexer)

    #Parte_del lexico
    def parte_Lexico(self,data):
        self.tokens = [] #Reinicia la lista de tokens
        self.errores_lexicos = []
        self.identificadores=[]
        self.varId=0 #poner un id al identificador
        self.lexi.lexer.lineno = 1 #Reincia el número de linea
        self.lexi.lexer.input(data) #Se pasa la información
        self.compilo = True #Si todo compilo bien
        while True:
            tok = self.lexi.lexer.token()
            if not tok:
                break
            self.tokens.append(tok)
            if tok.type == 'IDENTIFICADOR': #Agrega a la lista de identificadores
                    self.revisar_ts(tok)
            print(tok)
        self.errores_lexicos = self.lexi.errores
        self.lexi.errores=[]
        if self.errores_lexicos == []:
            self.compilo=True
        else:
            self.compilo=False
        self.identificadores_lista()

    def parte_Sintactica(self,data,lexer):
        self.sin.build()
        lexer.lineno = 1 #Reincia el número de linea
        try:
            resultado = self.sin.parser.parse(data, lexer=lexer ,tracking=True)
            if resultado:
                print("Análisis sintáctico exitoso:", resultado)
                #print("Análisis sintáctico completado pero sin resultado (posiblemente vacío)")
            if self.sin.errores !=[]:
                self.compilo = False
                self.errores_sintacticos=self.sin.errores
        except Exception as e:
            print(f"Error durante el análisis sintáctico: {e}")
    #Errores
    def errores_re(self):
        mensajes=''
        self.errores_lista = self.errores_lexicos+self.errores_sintacticos
        self.errores_lista= sorted(self.errores_lista, key=lambda x:x[2])
        for error in self.errores_lista:
            mensajes+=(f"{error[0]}" +'\n')
        return mensajes
    
    #Revisa la lista de identificadores, agrega el token y los ordena
    def revisar_ts(self,tok):
        for token in self.identificadores:
            if token[0].value == tok.value :
                return 
        self.varId += 1
        self.identificadores.append([tok,f"id{self.varId}"])
        self.identificadores = sorted(self.identificadores, key=lambda x: x[0].value)
                

    def identificadores_lista(self):
        self.identificadores_ts=[]
        for token in self.identificadores:
            self.identificadores_ts.append([token[0].value, token[1],'Sin tipo', 'Sin Valor'])
        return self.identificadores_ts

if __name__ == "__main__":
    # Define algunas pruebas
    pruebas = [
        'a = b',
        'n = 5',
        'array[1] = 3*5', 
        'i++',
        'numeros = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]',
        'cadenas = ["cadena1", "cadena2", "cadena3"]'
        'Clase objeto = new Clase(1, 2, 3)', 
        'bandera = this.metodoBooleano(x, z)',
        'a += 5',
        'arrar[3] == 3'
    ]
    compila = Compilador()

    # Ejecutar pruebas
    for prueba in pruebas:
        print(f"\nProbando: {prueba}")
        compila.compilar(prueba)