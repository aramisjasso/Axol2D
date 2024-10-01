class Semantico():
    def __init__(self):
        #Lista de errores
        self.errores = []
        self.compilo = True
        self.ts= [] # [token[0].value, token[1],'Sin tipo', 'Sin Valor','Linea declación']
        self.programa = None
        self.parteImportaciones = None
        self.parteNivel = None
        self.parteDeclaracion= None
        self.parteMetodos = None
        self.parteMetodoPrincipal = None
        self.listaDeclaraciones = []

    #Run
    def correr(self,resultadoSemantico,TS):
        self.programa =resultadoSemantico
        self.errores=[]
        self.compilo = True
        self.ts=TS
        self.fnSepararArbol()
        #self.fnParteImport()
        self.fnParteNivel()
        self.fnPrintTs()
        print('Fin Semantico')

    #Separa las partes de las tuplas
    def fnSepararArbol(self):
        for indice, valor in enumerate(self.programa):
            if indice !=0:
                if valor[0]== 'nivel':
                    self.parteNivel= valor
                if valor[0] == 'importaciones':
                    self.parteImportaciones = valor
        
        if self.parteNivel != None:
            for indice, valor in enumerate(self.parteNivel[2]):
                if indice !=0:
                    if valor[0]== 'bloqueDeclaracion':
                        self.parteDeclaracion = list(valor)
                        

                                                               
                    if valor[0] == 'bloqueMetodos':
                        self.parteMetodos = valor
                    if valor[0] == 'metodoPrincipal':
                        self.parteMetodoPrincipal = valor
                                
        
        
    #Parte de nivel
    def fnParteNivel(self):
        #Validación en TS del nombre de nivel
        self.fnDeclararTipo(self.parteNivel[1],'Nivel')
        self.fnBloqueDeclaracion()
        #self.bloqueMetodos 
        #self.metodoPrincipal

#---------Separación de bloque de Declaración ------------------------------------------------------
    def fnSeparacionDeclaracion(self):
        compara = True
        while(compara):
            print(self.parteDeclaracion)
            if len(self.parteDeclaracion[1]) == 2: #Declaraciones simples
                self.listaDeclaraciones.append((self.parteDeclaracion[1]))
            else:
                self.listaDeclaraciones.append((self.parteDeclaracion[1][1],self.parteDeclaracion[1][2]))

            if self.parteDeclaracion[2] is None:
                compara =False
                break
            self.parteDeclaracion = self.parteDeclaracion[2]

#---------Bloque declaración -----------------------------------------------------------------------
    def fnBloqueDeclaracion(self):
        print('Bloque Declaración')
        self.fnSeparacionDeclaracion()
        #Muestra una declaración una por una
        for declaracion in self.listaDeclaraciones:
            print(declaracion)
            estructura = None
            tipo = None
            tamaño = None
            id = None
            valores=None
            if declaracion[0][0] == 'declaracionTipo':
                id=declaracion[0][2]
                tipo=declaracion[0][1]
                #Declaracion
                self.fnDeclararTipo(id,tipo)
                if len(declaracion)==2:
                    valores= declaracion[1]
                    #Asignacion
                    self.fnAsignar(valores,id)
            if declaracion[0][0] == 'declaracionEstructuraDatos':
                estructura = declaracion[0][1][0]
                tipo = declaracion[0][1][1][1]
                tamaño = declaracion[0][1][1][3]
                id= declaracion[0][1][1][2]
                print(estructura,tipo,id,tamaño)
                #Declaracion
                self.fnDeclararEstructuraDatos(estructura,tipo,id,tamaño)
                if len(declaracion[0][1])==3:
                    #Asignacion
                    valores=declaracion[0][1][2]
                    self.fnAsignar(valores,id)
        
# ------------ Encuentra el tipo de ts -------------------------------------------------------------
    def fnEncontrarTipo(self,id):
        for simbolo in self.ts:
            # [token[0].value, token[1],'Sin tipo', 'Sin Valor','Linea declación']
            if simbolo[0]==id:
                return simbolo[2]

# ------------ Devuelve True si ya fue declarado --------------------------------------------------
    # Devuelve un true si fue declaro el id 
    def fnComprobarDeclaracion(self,id):
        for simbolo in self.ts:
            # [token[0].value, token[1],'Sin tipo', 'Sin Valor','Linea declación']
            if simbolo[0]==id:
                if simbolo[2] !='Sin tipo':
                    return True
        return False

#----------- Declracion en TS  por tipo -----------------------------------------------------
    def fnDeclararTipo(self,id,tipo,var=None):
        if not(self.fnComprobarDeclaracion(id)):
            for indice,simbolo in enumerate(self.ts):
                if simbolo[0]==id:
                    simbolo[2]=tipo
                    break
            if tipo[0]=='arreglo':
                self.ts[indice][3]=var
                for x in range(int(var)):
                    in_simbolo=[f'{id},{x}',f'{simbolo[1]},{x}',tipo[1],'Null', 'Linea declaración']
                    self.ts.insert(indice+x+1,in_simbolo)
            if tipo[0]=='matriz':
                self.ts[indice][3]=var
                for x in range(int(var[0])):
                    for y in range(int(var[1])):
                        in_simbolo=[f'{id},{x},{y}',f'{simbolo[1]},{x},{y}',tipo[1],'Null', 'Linea declaración']
                        self.ts.insert(indice+1,in_simbolo)
                        indice+=1       
        else:
            #Error dos veces declarado
            self.compilo = False
            tipoEn =self.fnEncontrarTipo(id)
            self.errores.append([f'Error Semántico el identificador {id} ya habia sido declarado anteriormente de tipo {tipoEn}',0,1])

#----------- Declaracion en TS por Estructura de Datos ----------------------------------
    def fnDeclararEstructuraDatos(self,estructura,tipo,id,tamaño):
        if estructura=='declaracionArreglo':
            tipo = ('arreglo',tipo)
            self.fnDeclararTipo(id,tipo,tamaño)
        if estructura=='declaracionMatriz':
            tipo=('matriz',tipo)
            self.fnDeclararTipo(id,tipo,tamaño)


#----------Asignacion en TS de Estructura de Datos--------------------------------------
    def fnAsignar(self,valores,id):
        #falta validar su declaración
        #indice
        indice=self.fnIndice(id)
        tipo_id=self.ts[indice][2]
        
        #Validad si el id es del tipo que se pasa
        #Validar si es arreglo o método
        if len(tipo_id)==2:
            
            tipo=valores[0]
            if tipo=='fila':
                tipo='arreglo'
            elif tipo=='filas':
                tipo='matriz'
            else:
                self.errores.append([f'Error Semántico, el valor no puede ser asignado a un arreglo, una matriz o un identificador.'])
            #Sacar tipo de valores
            
            #Validar si es arreglo, matriz o método
            if tipo_id[0]=='metodo':
                self.errores.append([f'Error Semántico al identificador {id} es de tipo método y no se puede asignar nigún valor.',0,1])
                return
            elif tipo_id[0]=='arreglo':
                if tipo != tipo_id[0]:
                  self.errores.append([f'Error Semántico al identificador {id} es de tipo Arreglo y no se puede asignar una Matriz.',0,1])
                else:
                    #Validación por Tamaño
                    tamaño=int(valores[1])
                    tamaño_arreglo=int(self.ts[indice][3])
                    if tamaño_arreglo!=tamaño:
                        self.errores.append([f'Error Semántico, el tamaño de la fila no se puede asignar al identificador {id} el tamaño declaro es: {tamaño_arreglo}',0,1])
                    else:
                        for x in range(tamaño):
                            self.ts[indice+x+1][3]=valores[2][x]
            else:
                #Validacion Tipos
                if tipo != tipo_id[0]:
                    
                    self.errores.append([f'Error Semántico al identificador {id} es de tipo Matriz y no se puede asignar un Arreglo.',0,1])
                else:
                    #Validación por Tamaño
                    tamaño_matriz_x=int(self.ts[indice][3][0])
                    tamaño_matriz_y=int(self.ts[indice][3][1])
                    tamaño_x=int(valores[1][0])
                    tamaño_y=valores[1][1]
                    compara=int(tamaño_y[0])
                    print(tamaño_matriz_x,tamaño_matriz_y,tamaño_x,tamaño_y)
                    resultado=True
                    for x in tamaño_y:
                        if int(x) != compara:
                            resultado=False
                    #La filas son de diferentes tamaños entre si
                    if resultado is False:
                        self.errores.append([f'Error Semántico la matriz tiene filas con diferentes tamaños',0,1])
                    else:
                        if tamaño_matriz_x !=tamaño_x or tamaño_matriz_y!=compara:
                            self.errores.append([f'Error Semántico, las Matriz no se puede asignar al identificador {id} el tamaño declarado es de: {[tamaño_matriz_x,tamaño_matriz_y]}.',0,1])
                        else:
                            filas=valores[2]
                            for x in range(tamaño_matriz_x):
                                for y in range(tamaño_matriz_y):
                                    valor=filas[x][2][y]
                                    self.ts[indice+1][3] = valor
                                    indice+=1
                

                    print('Matriz')
        else:
            tipo=self.fnRegresaValor(valores,tipo_id)
            if tipo_id==tipo:
                self.ts[indice][3]=valores
            else:
                self.errores.append([f'Error Semántico, el valor no puede ser asignado al identificador.'])
                # string
                #     | BOOLEANO
                #     | CHAR
                #     | BYTE':
#---------Funcion que regresa tipo, NO FUNCIONA ES DE PRUEBA----------------------------
    def fnRegresaValor(self,valor,tipo):
        return tipo
#---------Vuelve indice de TS-----------------------------------------------------------
    def fnIndice(self,id):
        simbolo = None
        for indice, simbolo in enumerate(self.ts):
            if simbolo[0] == id:
                simbolo=indice
                break
        return simbolo

        

#---------Impresión TS------------------------------------------------------------------
    def fnPrintTs(self):
        print('Impresión de TS')
        for simbolo in self.ts:
            print(simbolo)
