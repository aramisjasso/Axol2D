import re

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
        self.listaParametros = []
        self.pila_semantica = []
        self.banderaStart = False

    #Run
    def correr(self,resultadoSemantico,TS):
        self.programa =resultadoSemantico
        self.errores=[]
        self.compilo = True
        self.ts=TS
        self.fnSepararArbol()
        self.fnParteImport()
        if self.parteNivel[2] != 'Sin Contenido Nivel':
            self.fnParteNivel()
        self.fnPrintTs()
        if len(self.errores)!=0:
            self.compilo=False
        print('Fin Semantico')

    #Separa las partes de las tuplas
    def fnSepararArbol(self):
        for indice, valor in enumerate(self.programa):
            if indice !=0:
                if valor[0]== 'nivel':
                    self.parteNivel= valor
                    #print('Nivel:',valor)
                if valor[0] == 'importaciones':
                    self.parteImportaciones = valor
                    #print('Importaciones:',valor)
        
        if self.parteNivel != None:
            #print(self.parteNivel[2])
            for indice, valor in enumerate(self.parteNivel[2]):
                if indice !=0:
                    if valor[0]== 'bloqueDeclaracion':
                        self.parteDeclaracion = list(valor)
                        #print('bloqueDeclaracion',valor)
                                                               
                    if valor[0] == 'bloqueMetodos':
                        self.parteMetodos = valor
                        #print('bloqueMetodos',valor) 

                    if valor[0] == 'metodoPrincipal':
                        self.parteMetodoPrincipal = valor
                                
    #Parte Import
    def fnParteImport(self):
        if self.parteImportaciones != None:
            listaImportaciones = self.parteImportaciones[1]
            for x in listaImportaciones:
                if x == 'Background':
                    self.fnIsertarImportaciones(x)
                elif x == 'Players':
                    self.fnIsertarImportaciones(x)

    # Insertar importaciones
    def fnIsertarImportaciones(self,tipo):
        if tipo == 'Background':
            if not self.fnChecharImportaciones('background',tipo):
                fondos = [
                ['Forest', 'id_import', 'background', 'Forest', 'Linea declación'],
                ['Mountain', 'id_import', 'background', 'Mountain', 'Linea declación'],
                ['Ocean', 'id_import', 'background', 'Ocean', 'Linea declación'],
                ['Desert', 'id_import', 'background', 'Desert', 'Linea declación'],
                ['City', 'id_import', 'background', 'City', 'Linea declación'],
                ['Village', 'id_import', 'background', 'Village', 'Linea declación'],
                ['Cave', 'id_import', 'background', 'Cave', 'Linea declación'],
                ['Swamp', 'id_import', 'background', 'Swamp', 'Linea declación'],
                ['River', 'id_import', 'background', 'River', 'Linea declación'],
                ['Island', 'id_import', 'background', 'Island', 'Linea declación'],
                ['Castle', 'id_import','background', 'Castle','Linea declación']]
                self.fnIsertarArrayImportaciones(fondos)
        else:
            if not self.fnChecharImportaciones('character',tipo):
                jugadores = [
                    ['wizard', 'id_import', 'character', 'wizard', 'Línea de declaración'],
                    ['archer', 'id_import', 'character', 'archer', 'Línea de declaración'],
                    ['rogue', 'id_import', 'character', 'rogue', 'Línea de declaración'],
                    ['paladin', 'id_import', 'character', 'paladin', 'Línea de declaración'],
                    ['barbarian', 'id_import', 'character', 'barbarian', 'Línea de declaración'],
                    ['assassin', 'id_import', 'character', 'assassin', 'Línea de declaración'],
                    ['druid', 'id_import', 'character', 'druid', 'Línea de declaración'],
                    ['samurai', 'id_import', 'character', 'samurai', 'Línea de declaración'],
                    ['ninja', 'id_import', 'character', 'ninja', 'Línea de declaración'],
                    ['priest', 'id_import', 'character', 'priest', 'Línea de declaración'],
                    ['knight', 'id_import','character', 'knight','Linea declación']
                ]
                self.fnIsertarArrayImportaciones(jugadores)


    # Checa si ya se hizo la declaración de importaciones
    def fnChecharImportaciones(self,tipo,lib):
        for x in self.ts:
            # [token[0].value, token[1],'Sin tipo', 'Sin Valor','Linea declación']
            if x[2] == tipo:
                self.errores.append([f'Error semantico, la librería {lib} ya ha sido importada.',0,1])
                return True # La librería ya fue declarada

    #Inserta todas las importaciones en orden alfabetico
    def fnIsertarArrayImportaciones(self,elementos):
        for x in elementos:
            indice =  self.fnIndice(x[0])
            if indice is None or isinstance(indice, list):
                self.ts.append(x)
            else:
                self.ts[indice]=x
        self.ts = sorted(self.ts, key=lambda x: x[0])
    #Parte de nivel
    def fnParteNivel(self):
        #Validación en TS del nombre de nivel
        self.fnDeclararTipo(self.parteNivel[1],'Nivel')
        self.fnBloqueDeclaracion()
        if not(self.parteMetodos is None):
            self.fnbloqueMetodos()
        if self.parteMetodoPrincipal[1] != 'Sin Método Axol': 
            self.fnMetodoPrincipal()

#---------Separación de bloque de Declaración ------------------------------------------------------
    def fnSeparacionDeclaracion(self):
        compara = True
        while(compara):
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
        self.fnSeparacionDeclaracion()
        #Muestra una declaración una por una
        for declaracion in self.listaDeclaraciones:
            estructura = None
            tipo = None
            tamaño = None
            id = None
            valores=None
            # Declaración de Variables Simples
            # Declaración sin Asignación
            if declaracion[0] == 'declaracion':
                id = declaracion[1][2]
                tipo = declaracion[1][1]
                self.fnDeclararTipo(id,tipo)
            # Declaración con Asignación
            if declaracion[0][0] == 'declaracionTipo':
                id=declaracion[0][2]
                tipo=declaracion[0][1]
                # Declaracion
                self.fnDeclararTipo(id,tipo)
                valores= declaracion[1]
                self.fnAsignar(valores,id)
            if declaracion[0][0] == 'declaracionEstructuraDatos':
                estructura = declaracion[0][1][0]
                tipo = declaracion[0][1][1][1]
                tamaño = declaracion[0][1][1][3]
                id= declaracion[0][1][1][2]
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
                if simbolo[2] != 'Sin tipo':
                    return True
                else:
                    return False
        return 'NoId'

#----------- Declaracion en TS  por tipo -----------------------------------------------------
    def fnDeclararTipo(self,id,tipo,var=None):
        if not(self.fnComprobarDeclaracion(id)):
            temp_errores = len(self.errores)
            for indice,simbolo in enumerate(self.ts):
                if simbolo[0]==id:
                    self.ts[indice][2]=tipo
                    break
            #Checa si es de un tipo arreglo
            if tipo[0]=='arreglo':
                if tipo[1]in ['obstacles','platform']:
                    self.ts[indice][3]=var
                    y = 0
                    for x in range(int(var)):
                        in_simbolo=[f'{id},{x}',f'{simbolo[1]},{x}',tipo[1],'Null', 'Linea declaración']
                        self.ts.insert(indice+y+1,in_simbolo)
                        y+=1
                        atributos=['0', '1', '2', '3',  '4'   ,  '5'   ,  '6'  ]
                        for k in range(len(atributos)):
                            in_simbolo=[f'{id},{x},{atributos[k]}',f'{simbolo[1]},{atributos[x]}','int','Null', 'Linea declaración']
                            self.ts.insert(indice+y+1,in_simbolo)
                            y+=1
                        
                else:
                    self.ts[indice][3]=var
                    for x in range(int(var)):
                        in_simbolo=[f'{id},{x}',f'{simbolo[1]},{x}',tipo[1],'Null', 'Linea declaración']
                        self.ts.insert(indice+x+1,in_simbolo)
            #Checa si es de un tipo matriz
            elif tipo[0]=='matriz':
                self.ts[indice][3]=var
                x1=0
                for x in range(int(var[0])):
                    for y in range(int(var[1])):
                        in_simbolo=[f'{id},{x},{y}',f'{simbolo[1]},{x},{y}',tipo[1],'Null', 'Linea declaración']
                        self.ts.insert(indice+x1+1,in_simbolo)
                        x1+=1
            #Checa si es de un tipo metodo
            elif tipo[0] == 'metodo':
                atributos = []
                x=0 #inicia x=0 para cuando no hay
                id_ts=self.ts[indice][1]
                #Validar que en los parametros no haya variables repetidas
                parametros=[]
                for x,valor in enumerate(self.listaParametros):
                    id_m = valor[1]
                    parametros.append(id_m)
                    
                #Se guarda la cantidad de errores
                temp_errores = len(self.errores)
                if len(parametros) != len(set(parametros)):
                    self.errores.append([f'Error semantico, hay parametros repetidos en el método {id}.',0,1])
                else:
                    for x,valor in enumerate(self.listaParametros):
                        id_m = valor[1]
                        #validar que no exista como variable local
                        if self.fnComprobarDeclaracion(id_m):
                            self.errores.append([f'Error semantico, el identificador {id_m} ya habia sido declarado anteriormente como variable global.',0,1])
                        else:
                            tipo_m = valor[0]
                            #añade a lista atributos
                            atributos.append(tipo_m)
                            # [token[0].value, token[1],'Sin tipo', 'Sin Valor','Linea declación']
                            simbolo = [f'{id},{id_m}',f'{id_ts},{id_m}',tipo_m,'Null','Linea declaración']
                            self.ts.insert(indice+x+1,simbolo)

                    if temp_errores == len(self.errores):
                        print('creación de un método',self.ts[indice])
                        self.ts[indice][3]=(x+1, atributos)
                        print('creación de un método',self.ts[indice])
            elif tipo in ['obstacles', 'platform']:
                atributos=['0', '1', '2', '3',  '4'   ,  '5'   ,  '6'  ]
                for x in range(len(atributos)):
                    in_simbolo=[f'{id},{atributos[x]}',f'{simbolo[1]},{atributos[x]}','int','Null', 'Linea declaración']
                    self.ts.insert(indice+x+1,in_simbolo)
                #self.ts[indice][3]=tipo
            elif tipo == 'player':
                #[inicio_x, inicio_y, vidas, personaje]
                atributos=[['inicio_x','int'], ['inicio_y','int'], ['vidas','int'], ['personaje','character']]
                for x in range(len(atributos)):
                    in_simbolo=[f'{id},{atributos[x][0]}',f'{simbolo[1]},{atributos[x][0]}',atributos[x][1],'Null', 'Linea declaración']
                    self.ts.insert(indice+x+1,in_simbolo)
                self.ts[indice][3]=tipo
                #
        else:
            #Error dos veces declarado
            self.compilo = False
            if id == 'Sin Nivel':
                return
            tipoEn =self.fnEncontrarTipo(id)
            self.errores.append([f'Error Semántico. El identificador [{id}] ya ha sido declarado de tipo [{tipoEn}]. No puede declarar dos veces el mismo identificador. ',0,1])
        #if temp_errores ==len(self.errores):
            #Lo declara en la TS
            
            

#----------- Declaracion en TS por Estructura de Datos ----------------------------------
    def fnDeclararEstructuraDatos(self,estructura,tipo,id,tamaño):
        if estructura=='declaracionArreglo':
            tipo = ('arreglo',tipo)
            self.fnDeclararTipo(id,tipo,tamaño)
        if estructura=='declaracionMatriz':
            tipo=('matriz',tipo)
            self.fnDeclararTipo(id,tipo,tamaño)

#----------Asignacion en TS de Estructura de Datos--------------------------------------
    def fnAsignar(self,valores,id,inMetodo = False, var = None,renin=None):
        #Validar su declaración
        indice=self.fnIndice(id)
        tipo_id=self.ts[indice][2]
        #print('calcular valores adentro, ',valores,id,tipo_id,indice,self.ts[indice])
        #Validad si el id es del tipo que se pasa
        #Validar si es arreglo o método
        if len(tipo_id)==2 and renin is None:
            #print(tipo_id)
            tipo=valores[0]
            if tipo=='fila':
                tipo='arreglo'
            elif tipo=='filas':
                tipo='matriz'
            else:

                self.errores.append([f'Error Semántico, el valor no puede ser asignado a un arreglo, una matriz o un identificador.', 0, 1])
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
                        self.errores.append([f'Error Semántico, la fila no se puede asignar al identificador {id} los tamaños no coinciden el tamaño declaro es: {tamaño_arreglo}',0,1])
                    else:
                        if tipo_id[1]in['obstacles', 'platform']:
                            tamaño_errores = len(self.errores)
                            temp_valores=[]
                            #validar tipo
                            for x in range(tamaño):
                                temp_id = self.ts[indice+x*8+1][0]
                                temp_valores.append(self.ts[indice+x+1][3])
                                temp_valor = valores[2][x]
                                self.fnAsignar(temp_valor,temp_id, inMetodo,var)
                                #print('valor temporal',temp_valor,'id a actualizar',temp_id, inMetodo,var)
                                    #self.ts[indice+x+1][3]=temp_valor[1][1]
                                #self.ts[indice+x+1][3]=valores[2][x]
                            if tamaño_errores != len(self.errores) or inMetodo:
                                for x in range(tamaño):
                                    self.ts[indice+x+1][3]=temp_valores[x]
                        else:#Validación de inserción
                            tamaño_errores = len(self.errores)
                            temp_valores=[]
                            for x in range(tamaño):
                                temp_id = self.ts[indice+x+1][0]
                                temp_valores.append(self.ts[indice+x+1][3])
                                temp_valor = valores[2][x]
                                self.fnAsignar(temp_valor,temp_id,inMetodo,var)
                                #self.ts[indice+x+1][3]=valores[2][x]
                            if tamaño_errores != len(self.errores) or inMetodo:
                                for x in range(tamaño):
                                    self.ts[indice+x+1][3]=temp_valores[x]
                        

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
                    lista_numero=[]
                    resultado=True
                    for x in tamaño_y:
                        lista_numero.append(int(x))
                    compara_1 = lista_numero[0]
                    for x in lista_numero:
                        if compara_1!=x:
                            resultado=False

                    #La filas son de diferentes tamaños entre si
                    if resultado is False:
                        self.errores.append([f'Error Semántico la matriz tiene filas con diferentes tamaños',0,1])
                    else:
                        #Los tamaños son diferentes
                        compara=False
                        if all( num == tamaño_matriz_y for num in lista_numero):
                            compara = True
                            
                        if tamaño_matriz_x !=tamaño_x or not compara:
                            self.errores.append([f'Error Semántico, las Matriz no se puede asignar al identificador {id} el tamaño declarado es de: {[tamaño_matriz_x,tamaño_matriz_y]}.',0,1])
                        else:
                            filas=valores[2]
                            tamaño_errores = len(self.errores)
                            temp_valores=[]
                            x1=0
                            for x in range(tamaño_matriz_x):
                                for y in range(tamaño_matriz_y):
                                    valor=filas[x][2][y]
                                    temp_id=self.ts[indice+x1+1][0]
                                    #Se guarda el valor temporalmente para ver si no se debe de volver a poner
                                    temp_valor=self.ts[indice+x1+1][3]
                                    temp_valores.append(temp_valor)
                                    #Asignar valor
                                    self.fnAsignar(valor,temp_id,inMetodo,var)

                                    x1+=1
                                
                            #En caso de error
                            if tamaño_errores != len(self.errores) or inMetodo:
                                x1=0       
                                for x in range(tamaño_matriz_x):
                                    for y in range(tamaño_matriz_y):
                                        self.ts[indice+x1+1][3]=temp_valores[x1]
                                        x1+=1
                                 
        else:
            if renin:
                tipo_id=tipo_id[1]
            # tipo=self.fnRetornaValor(valores,tipo_id)
            if tipo_id in ['int', 'byte', 'boolean', 'char', 'string','obstacles', 'platform','background','character']:
                    #Valida que sea un arreglo el que se manda
                tipo=valores[0]
                valortemp = valores 
                if tipo == 'fila' and tipo_id in ['obstacles', 'platform']:
                    #print ('Entro en filas',id)
                    #Validación por Tamaño
                    tamaño=int(valores[1])
                    tamaño_arreglo= 7
                    #[Tam_x, Tam_y, posi_x, posi_y,  R   ,  G   ,  B  ]
                    if tamaño_arreglo!=tamaño:
                        self.errores.append([f'Error Semántico, la fila no se puede asignar al identificador {id} de tipo de {tipo_id} solo se pueden asignar arreglos de tamaño: {tamaño_arreglo}',0,1])
                    else:#Validación de inserción
                        tamaño_errores = len(self.errores)
                        temp_valores=[]
                        for x in range(tamaño):
                            temp_id = self.ts[indice+x+1][0]
                            temp_valores.append(self.ts[indice+x+1][3])
                            temp_valor = valores[2][x]
                            self.fnAsignar(temp_valor,temp_id,inMetodo,var)
                            #self.ts[indice+x+1][3]=valores[2][x]
                        if tamaño_errores != len(self.errores) or inMetodo:
                            for x in range(tamaño):
                                self.ts[indice+x+1][3]=temp_valores[x]
                        else:
                            self.ts[indice][3] = 'asignadoblo'
                
                elif tipo == 'fila' and tipo_id =='player':
                    #Validación por Tamaño
                    tamaño=int(valores[1])
                    tamaño_arreglo= 4
                    #[inicio_x, inicio_y, vidas, personaje]
                    if tamaño_arreglo!=tamaño:
                        self.errores.append([f'Error Semántico, la fila no se puede asignar al identificador {id} de tipo de {tipo_id} solo se pueden asignar arreglos de tamaño: {tamaño_arreglo}',0,1])
                    else:#Validación de inserción
                        tamaño_errores = len(self.errores)
                        temp_valores=[]
                        for x in range(tamaño):
                            temp_id = self.ts[indice+x+1][0]
                            temp_valores.append(self.ts[indice+x+1][3])
                            temp_valor = valores[2][x]
                            self.fnAsignar(temp_valor,temp_id,inMetodo,var)
                            #self.ts[indice+x+1][3]=valores[2][x]
                        if tamaño_errores != len(self.errores) or inMetodo:
                            for x in range(tamaño):
                                self.ts[indice+x+1][3]=temp_valores[x]

                # Asignación de una Expresión
                #print(valores)
                if valores[0] == 'expresion' and valores[1] != 'error':
                    #print(valores)
                    self.postorden(valores)
                    #print(self.pila_semantica)
                    valores = self.evaluar_pila(self.pila_semantica,var)
                    #print(valores)
                    # self.ts[indice][3] = self.pila_semantica
                    self.pila_semantica = []

                # Asignación de un Valor Diferente a Expresión
                # String, Char, Llamada a Método, Booleano
                if tipo != 'fila':

                    if not isinstance(valores, bool) and isinstance(valores, int) and tipo_id == 'int':
                        if (valores >= 0 and valores <= 65535):
                            if inMetodo is False:
                                self.ts[indice][3] = valores
                        elif valores < 0:
                            self.errores.append([f'Error Semántico. Axol2D no permite números negativos. El valor de la asignación será redondeado a 0. ', 0, 1])
                            if inMetodo is False:
                                self.ts[indice][3] = 0
                        else: 
                            self.errores.append([f'Error Semántico. El máximo valor permitido para una variable de tipo [int] es de 65535. ', 0, 1])
                    elif not isinstance(valores, bool) and isinstance(valores, int) and tipo_id == 'byte':
                        if valores >= 0 and valores <= 255:
                            if inMetodo is False:
                                self.ts[indice][3] = valores
                        elif valores < 0:
                            self.errores.append([f'Error Semántico. Axol2D no permite números negativos. El valor de la asignación será redondeado a 0. ', 0, 1])
                            if inMetodo is False:
                                self.ts[indice][3] = 0
                        else: 
                            self.errores.append([f'Error Semántico. El máximo valor permitido para una variable de tipo [byte] es de 255. ', 0, 1])
                    elif not isinstance(valores, tuple) and isinstance(valores, str) and re.fullmatch("'[a-zA-ZñÑ0-9]'", valores) and tipo_id == 'char':
                        if inMetodo is False:
                            self.ts[indice][3] = valores
                    elif isinstance(valores, str) and tipo_id == 'string' and valores != 'Null' and not re.fullmatch("'[a-zA-ZñÑ0-9]'", valores):
                        if inMetodo is False:
                            self.ts[indice][3] = valores
                    elif valores in ['true', 'false'] and tipo_id == 'boolean':
                        if valores:
                            self.ts[indice][3] = 'true'
                        else: 
                            self.ts[indice][3] = 'false'
                    elif isinstance(valores, tuple) and valores[0] == 'booleano' and tipo_id == 'boolean':
                        #print('valores:',valores,'valores:',valores[0],'tipo',tipo_id,id)
                        if inMetodo is False:
                            self.ts[indice][3] = valores[1]
                    elif valores=='asignadoblo' and tipo_id in ['platform','obstacles']:
                        id_buscar = valortemp[1][1]
                        indice_buscar = self.fnIndice(id_buscar)
                        for x in range(8):
                            #print('Donde guardar:', self.ts[indice_buscar+x][3],self.ts[indice+x][3])
                            self.ts[indice+x][3]=self.ts[indice_buscar+x][3]
                        #print('valores:',valores,'valores:',valores[0],'tipo',tipo_id,id, 'valor tempo', valortemp[1][1])

                    elif tipo_id =='background' and valores in ['Forest', 'Mountain', 'Ocean', 'Desert', 'City', 'Village', 'Cave','Swamp', 'River', 'Island','Castle']:
                        self.ts[indice][3] = valores
                    elif tipo_id =='character' and valores in ['wizard', 'archer', 'rogue', 'paladin', 'barbarian','assassin', 'druid', 'samurai', 'ninja', 'priest', 'knight']:
                        self.ts[indice][3] = valores
                        # buscar id que se asigana
                        

                    # elif isinstance(valores, list) and self.ts[indice][2] in ['int', 'byte']:
                    #     #Error de inicialización
                    #     self.ts[indice][3] = valores
                    else:
                        #print('valores:',valores,'valores:',valores[0],'tipo',tipo_id)
                        if valores != 'Null':
                            if not isinstance(valores, tuple):
                                #print(valores)
                                if isinstance(valores, bool) and valores: 
                                    valores = 'true'
                                elif isinstance(valores, bool) and not valores:  
                                    valores = 'false'
                                self.errores.append([f'Error Semántico. El tipo de dato [{tipo_id}] no coincide con el tipo de dato del valor asignado [{valores},].', 0, 1])  
                            elif valores[1] != 'error': 
                                self.errores.append([f'Error Semántico. El tipo de dato [{tipo_id}] no coincide con el tipo de dato del valor asignado [{valores[1]}].', 0, 1])  
                    #Si es de un tipo especial pero no array:

            
#---------Funcion que Retorna Valor----------------------------
    def fnRetornaValor(self, id):
        for simbolo in self.ts:
            # [token[0].value, token[1],'Sin tipo', 'Sin Valor','Linea declación']
            if simbolo[0] == id:
                return simbolo[3]
    
#-----------Bloque Metodos--------------------------------------------------------------
    def fnbloqueMetodos(self):
        lista_metodos=self.fnSeparacionMetodos()
        for x in lista_metodos:
                metodo=x
                id = metodo[2]
                tipo= metodo[1]
                tipo=('metodo',tipo)
                parametros = metodo[3]
                #Separación de Parametros
                self.fnSeparacionDeParametros(parametros[1])
                #Declaracion Métodos
                self.fnDeclararTipo(id,tipo,self.listaParametros)
                contenido = metodo[4]
                if len(contenido) == 3: 
                    instrucciones=contenido[1]
                    self.fnInstrucciones(instrucciones, id)
                    parteReturn=contenido[2]
                else: 
                    parteReturn=contenido[1]
                self.fnReturn(parteReturn,id)

                
        #print(lista_metodos)
        # if lista_metodos[0]=='metodo':#si la lista tiene solo un método
        #     metodo=lista_metodos[1]
        #     id = metodo[2]
        #     tipo= metodo[1]
        #     tipo=('metodo',tipo)
        #     parametros = metodo[3]
        #     #Separación de Parametros
        #     self.fnSeparacionDeParametros(parametros[1])
        #     #Declaracion Métodos
        #     self.fnDeclararTipo(id,tipo,self.listaParametros)
        #     contenido = metodo[4]
        #     if len(contenido) == 3: 
        #         instrucciones=contenido[1]
        #         self.fnInstrucciones(instrucciones, id)
        #         parteReturn=contenido[2]
        #     else: 
        #         parteReturn=contenido[1]
        #     self.fnReturn(parteReturn,id)
        # else:#Si la lista tiene más metodos
            
            

#---------Separación de Métodos -------------------------------------------------------
    def fnSeparacionMetodos(self):
        listaMetodos=self.parteMetodos[1]
        return listaMetodos

#---------Separación de Parametros ----------------------------------------------------
    def fnSeparacionDeParametros(self,parametros):
        self.listaParametros = []
        compara = True
        while(compara):
            if parametros is not None:
                if len(parametros[0])==2 :
                    self.listaParametros.append(parametros[0][1])
                    parametros = parametros[1]
                else:
                    self.listaParametros.append(parametros[1])
                    compara = False
            else:
                    compara=False

#---------Procesado de instrucciones----------------------------------------------------
    def fnInstrucciones(self, instrucciones, llamada):
        # print('Instrucciones',instrucciones)
        lista_instrucciones=[]
        for x in range(len(instrucciones)):
            instruccion=instrucciones[x][1]
            # print('Instrucciones',instruccion)
            lista_instrucciones.append(instruccion)
        
        #Se analizan todas las intrucciones para ver su tratamiento
        #print(lista_instrucciones)
        for x in lista_instrucciones:
            #print(lista_instrucciones)
            if x[0] == 'estructuraControl':
                if x[1][0] == 'ifElse': 
                    condicion = x[1][1]
                    print(condicion)
                    if x[1][1][1] != 'error':
                        self.postorden(condicion)
                        print(self.pila_semantica)
                        self.evaluar_pila(self.pila_semantica, llamada)
                        #condicionEvaluada = self.evaluar_pila(self.pila_semantica)
                        self.pila_semantica = []

                    #if con instrucciones sin else (o else sin instrucciones)
                    if len(x[1]) == 3: 
                        self.fnInstrucciones(x[1][2], llamada)
                    #Condición, instrucciones del if y else
                    elif len(x[1]) == 4: 
                        self.fnInstrucciones(x[1][2], llamada)
                        self.fnInstrucciones(x[1][3], llamada)
                    
                elif x[1][0] == 'switch':
                    #Validar que x[1][1] esté declarada
                    if not self.fnComprobarDeclaracion((x[1][1])):
                        self.errores.append([f'Error Semántico. La variable [{(x[1][1])}] no ha sido declarada.', 0, 1])
                        return
                    #Validar que x[1][1] sea de tipo numérica
                    if not self.fnEncontrarTipo(x[1][1]) in ['int', 'byte']:
                        self.errores.append([f'Error Semántico. La estructura [switch] solo acepta variables numéricas como variable de control.', 0, 1])
                        return
                    #Advertir si x[1][1] no ha sido inicializada
                    if self.fnRetornaValor(x[1][1]) == 'Null':
                        self.errores.append([f'Advertencia. La variable [{x[1][1]}] no ha sido inicializada, por lo tanto tomará el valor actual en memoria.', 0, 1])
                    #print(x[1])
                # elif x[1][0] == 'for':
                #     print(x[1])
                elif x[1][0] == 'forEach':
                    #Validar que x[1][2] no esté declarada
                    decVarControl = self.fnComprobarDeclaracion(x[1][2]) 
                    if decVarControl and decVarControl != 'NoId':
                        self.errores.append([f'Error Semántico. La variable [{x[1][2]}] no puede ser utilizada como variable de control en la estructura [for each] porque ha sido declarada previamente. ', 0, 1])
                        return
                    #Validar que x[1][3] sea una estructura de datos
                    if not self.fnComprobarDeclaracion(x[1][3]):
                        self.errores.append([f'Error Semántico. La estructura de datos [{x[1][3]}] no ha sido declarada. ', 0, 1])
                        return
                    if x[1][3] == 'Sin Estructura':
                        if len(x[1]) == 5:
                            self.fnInstrucciones(x[1][4], llamada)
                        return
                    ed = self.fnEncontrarTipo(x[1][3])
                    if not (isinstance(ed, tuple) and ed[0] in ['arreglo', 'matriz']):
                        self.errores.append([f'Error Semántico. La variable [{x[1][3]}] no es una estructura de datos, por lo tanto no es posible recorrerla en la estructura de contol [for each]. ', 0, 1])
                        return
                    #Validar que x[1][1] y x[1][3] sean del mismo tipo
                    if x[1][1] == 'Sin Tipo':
                        if len(x[1]) == 5:
                            self.fnInstrucciones(x[1][4], llamada)
                        return
                    if not x[1][1] == ed[1]:
                        self.errores.append([f'Error Semántico. La variable de control de tipo [{x[1][1]}] no coincide con el tipo de dato de la estructura de control de tipo [{ed[1]}]. ', 0, 1])
                        return
                    
                    #for( n : numeros) { }
                    #acachar este error podría ser más específico

                    if len(x[1]) == 5:
                        self.fnInstrucciones(x[1][4], llamada)

                elif x[1][0] == 'while':
                    condicion = x[1][1]
                    self.postorden(condicion)
                    condEval = self.evaluar_pila(self.pila_semantica,llamada)
                    #print(condEval)
                    self.pila_semantica = []
                    #Evaluar instrucciones
                    if len(x[1]) == 3:
                         self.fnInstrucciones(x[1][2], llamada)
                elif x[1][0] == 'doWhile':
                    condicion = x[1][1]
                    self.postorden(condicion)
                    condEval = self.evaluar_pila(self.pila_semantica,llamada)
                    #print(condEval)
                    self.pila_semantica = []
                    #Evaluar instrucciones
                    if len(x[1]) == 3:
                        self.fnInstrucciones(x[1][2], llamada)

            elif x[0]=='expresionAsignacion':
                id=x[1][1]
                
                temp = self.fnComprobarDeclaracion(id)
                #print('id:',id)
                #print('Declaración antes', temp)
                if not temp or 'NoId'== temp:
                    #print('Declaración', temp)
                    temp_id=id
                    id=f'{llamada},{id}'
                    if 'NoId'== self.fnComprobarDeclaracion(id):
                        self.errores.append([f'Error Semántico. La variable [{temp_id}] no ha sido declarada.', 0, 1])
                else:        
                    if len(x)==3:
                        valores= x[2]
                        if x[2][0] == 'llamadaMetodo':
                            print('Aqui se hizo una llamada a Metodo' , x)
                            self.fnAsignar(valores,id,True, llamada,True)
                        else:
                            self.fnAsignar(valores,id,True, llamada)
                    elif len(x)==2:
                        valores= x[1][2]
                        self.fnAsignar(valores,id,True, llamada)
            elif x[0]=='llamadaMetodo':
                id = x[1]
                cantidad = x[2]
                argumentos = x[3]
                #Separacion de métodos propios y axol
                if id in ['READ_BIN', 'READ_TEC','SAVE_BIN','PRINT', 'PRINT_CON', 'SHOW', 'POSITIONX','POSITIONY', 'RANDOM', 'GETPOSITION']:
                    print('Método Axol')
                else:
                    self.fnLlamadaMetodo(x[1],x[2],x[3],llamada)
            elif x[0] == 'llamadaStart':
                if llamada != 'axol':
                    self.errores.append([f'Error Semántico. El método start() solo puede ser llamado desde el método principal axol2D play().', 0, 1])
                    return
                # print(self.ts[0][0])
                # print(x[1])
                if not (self.fnComprobarDeclaracion(x[1]) and self.fnEncontrarTipo(x[1]) == 'Nivel'):
                    if self.ts[0][2] == 'Nivel':
                        nombreNivel = self.ts[0][0]
                    else: 
                        nombreNivel = 'Nivel sin Idenficador'
                    self.errores.append([f'Error Semántico. El identificador de llamada al método start() [{x[1]}] no coincide con el identificador del nivel [{nombreNivel}].', 0, 1])
                    return
                self.banderaStart = True
                #print(x)

#----------Asignación Metodo ()--------------------------------------------------------------
    def fnLlamadaMetodo(self,id,cantidad,argumentos,id_desdellamado ):
        print('Es una llamada de Metodo', id, cantidad, argumentos)
        #Validación si es un método
        tipo=self.fnEncontrarTipo(id)
        if not (isinstance(tipo, tuple) and tipo[0] in ['metodo']):
            self.errores.append([f'Error Semántico. La variable llamada no es un método [{id}].', 0, 1])
            return
        #Validar cantidad de argumentos
        indice=self.fnIndice(id)
        cantidad_metodo = int(self.ts[indice][3][0])
        # print('Catidad método: ',cantidad_metodo)
        if cantidad!=cantidad_metodo:
            self.errores.append([f'Error Semántico. La cantidad de argumentos proporcionados, no corresponde con la cantidad de argumentos declarados.', 0, 1])
            return
        #Validar tipo de argumento
        lista_argumentos=self.fnListaArgumentos(argumentos,cantidad)
        for x in range(cantidad_metodo):
            temp_id=self.ts[indice+x+1][0]
            #print('indice: ',temp_id)
            #print('valor: ', lista_argumentos[x])
            self.fnAsignar(lista_argumentos[x],temp_id,True,id_desdellamado)

        # print('Tipo',tipo[1])
        #lista_argumentos = fnSeparacionArgumentos(argumentos)

#---------Lista de Argumentos --------------------------------------------------------
    def fnListaArgumentos(self,argumentos,cantidad):
        lista_argumentos=[]
        for x in range(cantidad):
            lista_argumentos.append(argumentos[1])
            if x<=cantidad-1:
                argumentos=argumentos[2]
        return lista_argumentos

 #---------Procesado de intrucciones----------------------------------------------------
    def fnReturn(self,regreso,id):
        # print('Return Metodo: ',id,regreso)
        #self.fnAsignar(regreso,id,True,id)
        # print('Retorno', regreso,id)
        self.fnAsignar(regreso,id,inMetodo = True, renin=True)#Porque el id nunca se puede llamar for

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

#-------------------------Recorrido de Condición en Postorden----------------------------
    def postorden(self, nodo):
        if isinstance(nodo, tuple):
            # Recorrer el hijo izquierdo primero
            if len(nodo) > 1:
                self.postorden(nodo[1])
            # Recorrer el hijo derecho
            if len(nodo) > 2:
                self.postorden(nodo[2])
            # Recorrer el hijo más a la derecha (por prioridad)
            if len(nodo) > 3:
                self.postorden(nodo[3])
            
            # Añadir el nodo actual a la pila después de los hijos
            if nodo[0] == 'factor' and not isinstance(nodo[1], tuple):
                self.pila_semantica.append(nodo[1]) 
            if nodo[0] == 'booleano':
                self.pila_semantica.append(nodo[1]) 
            if nodo[0] == 'valorCadena':
                self.pila_semantica.append(nodo[1]) 
            if nodo[0] == 'elementoExpresionLogica' and len(nodo) == 3:
                self.pila_semantica.append(nodo[2])
            elif nodo[0] == 'restoExpresionLogica':
                if len(nodo) == 3:
                    self.pila_semantica.append(nodo[1]) 
                else:
                    self.pila_semantica.append(nodo[2]) 
            elif nodo[0] == 'restoExpresionComparacion':
                if len(nodo) == 3:
                    self.pila_semantica.append(nodo[1])  
                else:
                    self.pila_semantica.append(nodo[2])
            elif nodo[0] == 'restoExpresionAritmetica':
                if len(nodo) == 3:
                    self.pila_semantica.append(nodo[1]) 
                else:
                    self.pila_semantica.append(nodo[2]) 
            elif nodo[0] == 'restoTermino':
                if len(nodo) == 3:
                    self.pila_semantica.append(nodo[1])  
                else:
                    self.pila_semantica.append(nodo[2])
            elif nodo[0] == 'expresionUnitaria':
                self.pila_semantica.append(nodo[2])
#---------------------------------------------------------------------------------------

#------------------------------Validación de Tipos---------------------------------------
    def validaNumero(self, elemento):
        try:
            int(elemento)
            return True
        except ValueError:
            return False
    
    def validaCadena(self, elemento):
        if elemento not in ['+', '-', '*', '/', '%', '==', '!=', '>', '<', '>=', '<=', '&', '|', '!']:
            return True
        return False
#-----------------------------------------------------------------------------------------------

#---------------------------Evaluación de la Pila Semántica-------------------------------------
    def evaluar_pila(self, semantica, nameMetod =None):
        pila_evaluacion = []
        idConValor = True
        
        for elemento in semantica:
            print(elemento)
            validaDeclaracion = self.fnComprobarDeclaracion(elemento)
            print(validaDeclaracion)
            
            if validaDeclaracion is False and nameMetod is not None:
                temp_elemento=elemento
                elemento=f'{nameMetod},{elemento}'
                validaDeclaracion = self.fnComprobarDeclaracion(elemento)
                print(validaDeclaracion)
                if validaDeclaracion == False or validaDeclaracion == 'NoId':
                    elemento=temp_elemento
                    print(elemento)
            
            validaDeclaracion = self.fnComprobarDeclaracion(elemento)
            if self.validaNumero(elemento):
                pila_evaluacion.append(int(elemento))
            #---Validación de Identificadores---
            elif isinstance(validaDeclaracion, bool):
                if validaDeclaracion: 
                    valor = self.fnRetornaValor(elemento)
                    if valor == 'Null':
                        self.errores.append([f'Advertencia. La variable [{elemento}] no ha sido inicializada, por lo tanto tomará el valor actual en memoria.', 0, 1])
                        pila_evaluacion.append(12) #Quitar esto cuando empecemos a trabajar con la memoria. 
                    else:
                        pila_evaluacion.append(valor)  
                else:
                    self.errores.append([f'Error Semántico. La variable [{elemento}] no ha sido declarada.', 0, 1])
                    return 'Null'
            elif elemento == 'true':
                pila_evaluacion.append(True)
            elif elemento == 'false':
                pila_evaluacion.append(False)
            elif self.validaCadena(elemento):
                pila_evaluacion.append(str(elemento))
            

            #Operadores Aritméticos
            elif elemento in ['+', '-', '*', '/', '%']:
                if len(pila_evaluacion) >= 2:
                    print(pila_evaluacion)
                    b = pila_evaluacion.pop()
                    a = pila_evaluacion.pop()
                    
                    if (isinstance(a, int)) and (isinstance(b, int)):
                        if elemento == '+':
                            resultado = a + b
                        elif elemento == '-':
                            resultado = a - b
                        elif elemento == '*':
                            resultado = a * b
                        elif elemento == '/':
                            if b != 0:
                                resultado = int(a / b)
                            else:
                                self.errores.append(['Error Semántico. No se puede dividir entre cero.', 0, 1])
                                return 'Null' 
                        elif elemento == '%':
                            if b != 0:
                                resultado = a % b
                            else:
                                self.errores.append(['Error Semántico. No se puede calcular el módulo de una división entre cero. ', 0, 1])
                                return 'Null' 
                        pila_evaluacion.append(resultado) 
                    else: 
                        if (isinstance(a, int)) or (isinstance(b, int)): 
                            if (isinstance(a, int)):
                                if not self.fnEncontrarTipo(b) in ['int', 'byte']:
                                    self.errores.append(['Error Semántico. Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ', 0, 1])
                                    return 'Null' 
                            if (isinstance(b, int)):
                                if not self.fnEncontrarTipo(a) in ['int', 'byte']:
                                    self.errores.append(['Error Semántico. Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ', 0, 1])
                                    return 'Null' 
                        else: 
                            if not self.fnEncontrarTipo(a) in ['int', 'byte'] or not self.fnEncontrarTipo(b) in ['int', 'byte'] :
                                self.errores.append(['Error Semántico. Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ', 0, 1])
                                return 'Null' 

            # Operadores de comparación
            elif elemento in ['==', '!=', '>', '<', '>=', '<=']:
                if len(pila_evaluacion) >= 2:
                    #Validar que son del mismo tipo
                    b = pila_evaluacion.pop()
                    a = pila_evaluacion.pop()
                    
                    if not (isinstance(a, bool) or (isinstance(b, bool))) and (((isinstance(a, int)) and (isinstance(b, int))) or (isinstance(a, str) and (isinstance(b, str)))):
                        if elemento == '==':
                            resultado = a == b
                        elif elemento == '!=':
                            resultado = a != b
                        elif elemento == '>':
                            resultado = a > b
                        elif elemento == '<':
                            resultado = a < b
                        elif elemento == '>=':
                            resultado = a >= b
                        elif elemento == '<=':
                            resultado = a <= b
                        pila_evaluacion.append(resultado) 
                    else: 
                        self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. La condición no fue evaluada. ', 0, 1])
                        return 'Null' 

                    # else: 
                    #     if (isinstance(a, int)) or (isinstance(b, int)): 
                    #         if (isinstance(a, int)):
                    #             if not self.fnEncontrarTipo(b) in ['int', 'byte']:
                    #                 self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. ', 0, 1])
                    #                 return 'Null' 
                    #         if (isinstance(b, int)):
                    #             if not self.fnEncontrarTipo(a) in ['int', 'byte']:
                    #                 self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. ', 0, 1])
                    #                 return 'Null' 
                    #     elif (isinstance(a, str)) or (isinstance(b, str)): 
                    #         if (isinstance(a, str)):
                    #             if self.fnEncontrarTipo(b) != 'string':
                    #                 self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. ', 0, 1])
                    #                 return 'Null' 
                    #         if (isinstance(b, str)):
                    #             if self.fnEncontrarTipo(a) != 'string':
                    #                 self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. ', 0, 1])
                    #                 return 'Null' 
                    #     elif (isinstance(a, bool)) or (isinstance(b, bool)): 
                    #         if (isinstance(a, bool)):
                    #             if self.fnEncontrarTipo(b) != 'boolean':
                    #                 self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. ', 0, 1])
                    #                 return 'Null' 
                    #         if (isinstance(b, bool)):
                    #             if self.fnEncontrarTipo(a) != 'boolean':
                    #                 self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. ', 0, 1])
                    #                 return 'Null' 
                    #     elif self.fnEncontrarTipo(a) != self.fnEncontrarTipo(b):
                    #         self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. ', 0, 1])
                    #         return 'Null' 
            # Operadores Lógicos
            elif elemento in ['&', '|']:
                if len(pila_evaluacion) >= 2:
                    #Validar que son booleanos
                    b = pila_evaluacion.pop()
                    a = pila_evaluacion.pop()
                    
                    if isinstance(a, bool) and isinstance(b, bool):
                        if elemento == '&':
                            resultado = a and b
                        elif elemento == '|':
                            resultado = a or b
                        pila_evaluacion.append(resultado)
                    if (isinstance(a, bool)) or (isinstance(b, bool)): 
                        if (isinstance(a, bool)):
                            if self.fnEncontrarTipo(b) == 'boolean':
                                return 'Null' 
                        if (isinstance(b, bool)):
                            if self.fnEncontrarTipo(a) != 'boolean':
                                return 'Null'
                    if self.fnEncontrarTipo(a) == 'boolean' and self.fnEncontrarTipo(b) == 'boolean':
                        return 'Null' 
                    else: 
                        self.errores.append(['Error Semántico. Las operaciones lógicas solo pueden ser realizadas entre tipos booleanos (boolean). ', 0, 1])
                        return 'Null' 
                    
            # Operador NOT
            elif elemento == '!':
                if len(pila_evaluacion) >= 1:
                    #Validar que son booleanos
                    a = pila_evaluacion.pop()

                    if a == bool:
                        resultado = not a
                        pila_evaluacion.append(resultado)  
                    # elif self.fnEncontrarTipo(b) != 'boolean':
                    #     self.errores.append(['Error Semántico. Las operaciones lógicas solo pueden ser realizadas entre tipos booleanos (boolean). ', 0, 1])
                    #     return 'Null' 

        # El último valor en la pila de evaluación es el resultado final
        if len(pila_evaluacion) == 1:
            return pila_evaluacion[0]
            # else:
            #     raise ValueError("Error Semántico. La pila de evaluación no se evaluó correctamente.")   
#-----------------------------------------------------------------------------------------------

#------Método Axol--------------------------------------------------------------------------------------------
    def fnMetodoPrincipal(self):
        # Procesar instrucciones
        print(self.parteMetodoPrincipal[1])
        self.fnInstrucciones(self.parteMetodoPrincipal[1], 'axol')
        if not self.banderaStart:
            self.errores.append([f'Error Sintáctico (Línea ). Faltan llamada al método [start] en el método Axol2D. ', 0, 1])


#------Delete Parametros--------------------------------------------------------------------------------------
    def fnDeleteParametros(self):
        x = True
        con = 0
        while x :
            if 'Sin tipo'==self.ts[con][2]:
                self.ts.pop(con)
                if not con < len(self.ts):
                    x=False
            else:
                con+=1
                if not con < len(self.ts):
                    x=False