import compilador.lexico as lexico
import compilador.sintactico as sintactico
import compilador.semantico as semantico
import compilador.codigo_intermedio as codigo_int
import compilador.ensamblador as asm
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
        self.compilo = True #Si compila
        self.varId = 0
        self.resultado=None
        self.sema = semantico.Semantico()
        self.codigoint = codigo_int.Intermedio()
        self.variables=[] #TS variables
        self.metodos=[] #TS metodos
        self.importaciones=[] #TS importaciones
        self.ensamblador = asm.ensamblador()

    def compilar(self,data):
        self.parte_Lexico(data)
        self.parte_Sintactica(data,self.lexi.lexer)
        self.parte_Semantica()
        if self.compilo:
            self.parte_Intermedia()
            self.separar_tablas()
            self.parte_Ensamblador()
        

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
            # print(tok)
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
            self.resultado = self.sin.parser.parse(data, lexer=lexer ,tracking=True)
            # self.resultado = self.sin.parser.parse(data, lexer=lexer ,debug=True,tracking=True)
            if self.resultado:
                '''print("Análisis sintáctico exitoso:", self.resultado, '\n')'''
                #print("Análisis sintáctico completado pero sin resultado (posiblemente vacío)")
            if self.sin.errores != []:
                self.compilo = False
                self.errores_sintacticos=self.sin.errores
        except Exception as e:
            '''print(f"Error durante el análisis sintáctico: {e}")'''

    def parte_Semantica(self):
        self.sema.correr(self.resultado,self.identificadores_ts)
        self.identificadores_ts=self.sema.ts
        if(not self.sema.compilo):
            self.compilo = False
    
    def parte_Intermedia(self):
        self.codigoint.correr(self.resultado,self.identificadores_ts)

    #Ensamblador
    def parte_Ensamblador(self):
        self.ensamblador.fnCorre(self.codigoint.pilaCodigo, self.variables)

    #Errores
    def errores_re(self):
        mensajes=''
        self.errores_lista = self.errores_lexicos
        self.errores_lista +=self.errores_sintacticos
        self.errores_lista +=self.sema.errores
        self.errores_lista= sorted(self.errores_lista, key=lambda x:x[1])
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
            self.identificadores_ts.append([token[0].value, token[1],'Sin tipo', 'Null'])
        return self.identificadores_ts
    
    #Separar en tablas de simbolos
    #Separar información de tablas:
    def separar_tablas(self):
        self.variables=[]
        self.metodos=[]
        self.importaciones=[]
        for id in self.identificadores_ts:
            tipo =id[2]
            id_separado = id[0].split(",")
            
            if tipo in ["character","background"]:
                self.importaciones.append(id)
            elif (len(tipo) == 2 and tipo[0] == "metodo" ) or (len(id_separado)==2 and not id_separado[1].isdigit()):
                self.metodos.append(id)
            elif tipo == "Nivel":
                """No hace nada"""
            elif tipo == "string":
                id[3] = self.ajustar_cadena(id[3])
                self.variables.append(id)
            else:
                self.variables.append(id)

    def ajustar_cadena(self, cadena):
        cadena = str(cadena)
        tamaño = len(cadena)
        cadena = cadena[:tamaño-1]
        cadena = cadena[1:]
        if tamaño-1 > 50:
            # Truncar la cadena si es demasiado larga
            return cadena[:50]
        else:
            # Rellenar con espacios si es más corta
            return cadena.ljust(50)