class ensamblador():
    def __init__(self):
        self.codigo = [] #Código a imprimir
        self.codigoIntermedio = [] #Código pasado
        self.codigoConvertido = ""
        self.importaciones = []
        self.axol = []
        self.procedimientos = []
        self.TS =[]

    
    #Correr ensablador
    def fnCorre(self,codigoIntermedio, TS):
        self.codigoIntermedio = codigoIntermedio
        self.codigo = [] #Código a imprimir
        self.codigoConvertido = ""
        self.importaciones = []
        self.axol = []
        self.procedimientos = []
        self.TS = TS
        print("Inicio Ensamblador")
        self.codigo.append(""";---Ruiz Jasso Gerrardo Aramis---
;---López Ramírez Miguel Ángel---""")
        self.fnConversionCodigo()

        self.codigo.append(""";---Ruiz Jasso Gerrardo Aramis---
;---López Ramírez Miguel Ángel---""")
        self.fnImprimirConversion() #imprimir conversion
        self.fnCodigoConvertido() #imprimir en pantalla
        print("Fin Ensamblador")

    #Convertir código a ensamblador
    def fnConversionCodigo(self):
        
        self.fnSepararCodigo()
        self.fnImportaciones()
        self.fnTablaDeSimbolos()
        # self.fnCodigo()
        # self.fnProcedimientos()
    
    #Separa código en partes
    def fnSepararCodigo(self):
        compara = True
        contador = 0
        #Separa importaciones
        while (compara):
            elemento = self.codigoIntermedio[contador]
            if elemento[1][0] == "import":
                self.importaciones.append(elemento)
                contador += 1
            else:
                compara = False
        #Separar Axol
        compara = True
        while (compara):
            elemento = self.codigoIntermedio[contador]
            if elemento[1] == ('', '', ''):
                compara = False
                self.axol.append(elemento)
                contador += 1
            else:
                self.axol.append(elemento)
                contador += 1

        #Separar Metodos
        compara = True
        metodos = True
        tamaño_codigo = len(self.codigoIntermedio)
        while(metodos):
            metodo = []
            compara = True
            if tamaño_codigo > contador + 1:
                while (compara):
                    elemento = self.codigoIntermedio[contador]
                    if elemento[1] == ('', '', ''):
                        compara = False
                        metodo.append(elemento)
                        contador += 1
                    else:
                        metodo.append(elemento)
                        contador += 1
                self.procedimientos.append(metodo)
            else:
                metodos=False
            
    #Acomoda código
    def fnImportaciones(self):
        for importacion in self.importaciones:
            self.codigo.append(f"include {importacion[1][2]}")

    def fnTablaDeSimbolos(self):
        self.codigo.append(".DATA")
        compara = True
        contador = 0
        tamaño_TS = len(self.TS)
        while (compara):
            if tamaño_TS < contador + 1:
                compara = False
                break

            simbolo = self.TS[contador]
            id = simbolo[0]
            tipo = simbolo[2]
            
            #Tamaño
            tamaño = ""
            if simbolo[1] in [1, 50]:
                tamaño = "DB"
            elif simbolo [1] == 2 or tipo == "player" :
                tamaño = "DW"
            
            #Valor
            identificador = ""
            valor = ""
            
            #arreglo normal

            if len(tipo) == 2:
                if tipo[0] == "arreglo":
                    if tipo[1] in ["obstacles", "platform"]:
                        x = int(simbolo[3])
                        y = 7
                        
                        for elemento_x in range(x):
                            valor = ""
                            contador += 1
                            for elemento_y in range(y):
                                contador += 1
                                simbolo = self.TS[contador]
                                valor += f"{simbolo[3]} "
                            if elemento_x == 0:
                                identificador = f"\t{id} {tamaño} {valor}"
                            else:
                                identificador += f"\n\t{tamaño} {valor}"
                    else:
                        for elemento in range(int(simbolo[3])):
                            contador += 1
                            simbolo = self.TS[contador]
                            valor += f"{simbolo[3]} "
                        
                        identificador = f"\t{id} {tamaño} {valor}"
                else:
                    x = int(simbolo[3][0])
                    y = int(simbolo[3][1])
                    
                    for elemento_x in range(x):
                        valor = ""
                        for elemento_y in range(y):
                            contador += 1
                            simbolo = self.TS[contador]
                            valor += f"{simbolo[3]} "
                        if elemento_x == 0:
                            identificador = f"\t{id} {tamaño} {valor}"
                        else:
                            identificador += f"\n\t{tamaño} {valor}"
                        
            elif tipo in ["obstacles", "platform"]:
                for elemento in range(7):
                    contador += 1
                    simbolo = self.TS[contador]
                    valor += f"{simbolo[3]} "
                
                identificador = f"\t{id} {tamaño} {valor}"
            
            elif tipo in ["player"]:
                for elemento in range(3):
                    contador += 1
                    simbolo = self.TS[contador]
                    valor += f"{simbolo[3]} "
                
                identificador = f"\t{id} {tamaño} {valor}"
            elif tipo in ["string"]:
                valor = f"\"{simbolo[3]}\""
                identificador = f"\t{id} {tamaño} {valor}"
            else:
                valor = f"{simbolo[3]}"
                identificador = f"\t{id} {tamaño} {valor}"
            self.codigo.append(identificador)
            contador += 1
# ----------------------------------------------------------------------------------------------------------------------------------------------------------
    #Imprimir conversion
    def fnImprimirConversion(self):
        for icono in self.codigo:
            print(icono)
    
    #Convercion de código para mostrar en consola
    def fnCodigoConvertido(self):
        temporal = ""
        for icono in self.codigo:
            temporal += icono +"\n"
        self.codigoConvertido = temporal