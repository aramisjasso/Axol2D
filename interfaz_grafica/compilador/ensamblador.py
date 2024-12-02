class ensamblador():
    def __init__(self):
        self.codigo = [] #Código a imprimir
        self.codigoIntermedio = [] #Código pasado
        self.codigoConvertido = ""
        self.importaciones = []
        self.axol = []
        self.procedimientos = []

    
    #Correr ensablador
    def fnCorre(self,codigoIntermedio, TS):
        self.codigoIntermedio = codigoIntermedio
        self.codigo = [] #Código a imprimir
        self.codigoConvertido = ""
        self.importaciones = []
        self.axol = []
        self.procedimientos = []
        print("Inicio Ensamblador")
        self.fnConversionCodigo()
        self.fnImprimirConversion() #imprimir conversion
        self.fnCodigoConvertido() #imprimir en pantalla
        print("Fin Ensamblador")

    #Convertir código a ensamblador
    def fnConversionCodigo(self):
        self.fnSepararCodigo()
        self.fnImportaciones()
        # self.fnTablaDeSimbolos()
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