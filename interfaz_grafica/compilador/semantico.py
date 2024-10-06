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
        if len(self.errores)!=0:
            self.compilo=False
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
        self.fnbloqueMetodos()
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
                    if temp_errores ==len(self.errores):
                        self.ts[indice][3]=(x+1, atributos)
        else:
            #Error dos veces declarado
            self.compilo = False
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
    def fnAsignar(self,valores,id):
        #falta validar su declaración
        #indice
        indice=self.fnIndice(id)
        tipo_id=self.ts[indice][2]
        
        #Validad si el id es del tipo que se pasa
        #Validar si es arreglo o método
        if len(tipo_id)==2:
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
                    else:#Validación de inserción
                        tamaño_errores = len(self.errores)
                        temp_valores=[]
                        for x in range(tamaño):
                            temp_id = self.ts[indice+x+1][0]
                            temp_valores.append(self.ts[indice+x+1][3])
                            temp_valor = valores[2][x]
                            self.fnAsignar(temp_valor,temp_id)
                            #self.ts[indice+x+1][3]=valores[2][x]
                        if tamaño_errores != len(self.errores):
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
                                    self.fnAsignar(valor,temp_id)

                                    x1+=1
                                
                            #En caso de error
                            if tamaño_errores != len(self.errores):
                                x1=0       
                                for x in range(tamaño_matriz_x):
                                    for y in range(tamaño_matriz_y):
                                        self.ts[indice+x1+1][3]=temp_valores[x1]
                                        x1+=1
                                 
        else:
            # tipo=self.fnRetornaValor(valores,tipo_id)
            if tipo_id in ['int', 'byte', 'boolean', 'char', 'string']:
                # Asignación de una Expresión
                #print(valores)
                if valores[0] == 'expresion':
                    #print(valores)
                    self.postorden(valores)
                    #print(self.pila_semantica)
                    valores = self.evaluar_pila(self.pila_semantica)
                    #print(valores)
                    # self.ts[indice][3] = self.pila_semantica
                    self.pila_semantica = []

                # Asignación de un Valor Diferente a Expresión
                # String, Char, Llamada a Método, Booleano
                if not isinstance(valores, bool) and isinstance(valores, int) and self.ts[indice][2] == 'int':
                    if valores >= 0 and valores <= 65535:
                        self.ts[indice][3] = valores
                    elif valores < 0:
                        self.errores.append([f'Error Semántico. Axol2D no permite números negativos. El valor de la asignación será redondeado a 0. ', 0, 1])
                        self.ts[indice][3] = 0
                    else: 
                        self.errores.append([f'Error Semántico. El máximo valor permitido para una variable de tipo [int] es de 65535. ', 0, 1])
                elif not isinstance(valores, bool) and isinstance(valores, int) and self.ts[indice][2] == 'byte':
                    if valores >= 0 and valores <= 255:
                        self.ts[indice][3] = valores
                    elif valores < 0:
                        self.errores.append([f'Error Semántico. Axol2D no permite números negativos. El valor de la asignación será redondeado a 0. ', 0, 1])
                        self.ts[indice][3] = 0
                    else: 
                        self.errores.append([f'Error Semántico. El máximo valor permitido para una variable de tipo [byte] es de 255. ', 0, 1])
                elif not isinstance(valores, tuple) and isinstance(valores, str) and re.fullmatch("'[a-zA-ZñÑ0-9]'", valores) and self.ts[indice][2] == 'char':
                    self.ts[indice][3] = valores
                elif isinstance(valores, str) and self.ts[indice][2] == 'string' and valores != 'Null' and not re.fullmatch("'[a-zA-ZñÑ0-9]'", valores):
                    self.ts[indice][3] = valores
                # elif isinstance(valores, bool) and self.ts[indice][2] == 'boolean':
                #     if valores:
                #         self.ts[indice][3] = 'true'
                #     else: 
                #         self.ts[indice][3] = 'false'
                elif isinstance(valores, tuple) and valores[0] == 'booleano' and self.ts[indice][2] == 'boolean':
                    self.ts[indice][3] = valores[1]
                # elif isinstance(valores, list) and self.ts[indice][2] in ['int', 'byte']:
                #     #Error de inicialización
                #     self.ts[indice][3] = valores
                else:
                    if valores != 'Null':
                        if not isinstance(valores, tuple):
                            #print(valores)
                            if isinstance(valores, bool) and valores: 
                                valores = 'true'
                            elif isinstance(valores, bool) and not valores:  
                                valores = 'false'
                            self.errores.append([f'Error Semántico. El tipo de dato [{tipo_id}] no coincide con el tipo de dato del valor asignado [{valores}].', 0, 1])  
                        else: 
                            self.errores.append([f'Error Semántico. El tipo de dato [{tipo_id}] no coincide con el tipo de dato del valor asignado [{valores[1]}].', 0, 1])  

#---------Funcion que Retorna Valor----------------------------
    def fnRetornaValor(self, id):
        for simbolo in self.ts:
            # [token[0].value, token[1],'Sin tipo', 'Sin Valor','Linea declación']
            if simbolo[0] == id:
                return simbolo[3]
    
#-----------Bloque Metodos--------------------------------------------------------------
    def fnbloqueMetodos(self):
        lista_metodos=self.fnSeparacionMetodos()
        #print(lista_metodos)
        if lista_metodos[0]=='metodo':#si la lista tiene solo un método
            metodo=lista_metodos[1]
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
                self.fnInstrucciones(instrucciones)
                parteReturn=contenido[2]
            else: 
                parteReturn=contenido[1]
            #self.fnReturn(parteReturn,id)
        else:#Si la lista tiene más metodos
            for x in lista_metodos:
                metodo=x[1]
                id = metodo[2]
                tipo= metodo[1]
                tipo=('metodo',tipo)
                parametros = metodo[3]
                #Separación de Parametros
                self.fnSeparacionDeParametros(parametros[1])
                #Declaracion Métodos
                self.fnDeclararTipo(id,tipo,self.listaParametros)
                contenido = metodo[4]
                #print(contenido)
                instrucciones=contenido[1]
                self.fnInstrucciones(instrucciones)
                parteReturn=contenido[2]
                #self.fnReturn(parteReturn,id)
            

#---------Separación de Métodos -------------------------------------------------------
    def fnSeparacionMetodos(self):
        listaMetodos=[]
        for x in self.parteMetodos[1]:
            listaMetodos.append(x)
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
    def fnInstrucciones(self,instrucciones):
        # print('Instrucciones',instrucciones)
        lista_instrucciones=[]
        for x in range(len(instrucciones)):
            instruccion=instrucciones[x][1]
            # print('Instrucciones',instruccion)
            lista_instrucciones.append(instruccion)
        #Se analizan todas las intrucciones para ver su tratamiento
        #print(lista_instrucciones)
        for x in lista_instrucciones: 
            if x[0] == 'estructuraControl':
                if x[1][0] == 'ifElse': 
                    condicion = x[1][1]
                    #print(condicion)
                    self.postorden(condicion)
                    #print(self.pila_semantica)
                    self.evaluar_pila(self.pila_semantica)
                    #condicionEvaluada = self.evaluar_pila(self.pila_semantica)
                    self.pila_semantica = []

                    #if con instrucciones sin else (o else sin instrucciones)
                    if len(x[1]) == 3: 
                        self.fnInstrucciones(x[1][2])
                    #Condición, instrucciones del if y else
                    elif len(x[1]) == 4: 
                        self.fnInstrucciones(x[1][2])
                        self.fnInstrucciones(x[1][3])
                    
                elif x[1][0] == 'switch':
                    print(x[1])
                elif x[1][0] == 'for':
                    print(x[1])
                elif x[1][0] == 'forEach':
                    #Validar que x[1][2] no esté declarada
                    if self.fnComprobarDeclaracion(x[1][2]):
                        self.errores.append([f'Error Semántico. La variable [{x[1][2]}] no puede ser utilizada como variable de control en la estructura [for each] porque ha sido declarada previamente. ', 0, 1])
                        return
                    #Validar que x[1][3] sea una estructura de datos
                    if not self.fnComprobarDeclaracion(x[1][3]):
                        self.errores.append([f'Error Semántico. La estructura de datos [{x[1][3]}] no ha sido declarada. ', 0, 1])
                        return
                    ed = self.fnEncontrarTipo(x[1][3])
                    if not (isinstance(ed, tuple) and ed[0] in ['arreglo', 'matriz']):
                        self.errores.append([f'Error Semántico. La variable [{x[1][3]}] no es una estructura de datos, por lo tanto no es posible recorrerla en la estructura de contol [for each]. ', 0, 1])
                        return
                    #Validar que x[1][1] y x[1][3] sean del mismo tipo
                    print(x[1])
                elif x[1][0] == 'while':
                    condicion = x[1][1]
                    self.postorden(condicion)
                    condEval = self.evaluar_pila(self.pila_semantica)
                    print(condEval)
                    self.pila_semantica = []
                    #Evaluar instrucciones
                    if len(x[1]) == 3:
                         self.fnInstrucciones(x[1][2])
                elif x[1][0] == 'doWhile':
                    condicion = x[1][1]
                    self.postorden(condicion)
                    condEval = self.evaluar_pila(self.pila_semantica)
                    print(condEval)
                    self.pila_semantica = []
                    #Evaluar instrucciones
                    if len(x[1]) == 3:
                         self.fnInstrucciones(x[1][2])

            elif x[0]=='expresionAsignacion':
                id=x[1][1]
                if not self.fnComprobarDeclaracion(id):
                    self.errores.append([f'Error Semántico. La variable [{id}] no ha sido declarada.', 0, 1])
                    return
                valores= x[2]
                self.fnAsignar(valores,id)
            # elif x[0]=='llamadaMetodo':
            #     print('Es una llamada de Metodo', x[1],x[2])
            elif x[0] == 'llamadaStart':
                print(x)

 #---------Procesado de intrucciones----------------------------------------------------
    def fnReturn(self,regreso,id):
        print('Return Metodo: ',id,regreso)

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
    def evaluar_pila(self, semantica):
        pila_evaluacion = []
        idConValor = True
        
        for elemento in semantica:
            #print(elemento)
            validaDeclaracion = self.fnComprobarDeclaracion(elemento)

            if self.validaNumero(elemento):
                pila_evaluacion.append(int(elemento))
            #---Validación de Identificadores---
            elif isinstance(validaDeclaracion, bool) and validaDeclaracion:
                valor = self.fnRetornaValor(elemento)
                if valor == 'Null':
                    self.errores.append([f'Advertencia. La variable [{elemento}] no ha sido inicializada, por lo tanto tomará el valor actual en memoria.', 0, 1])
                    pila_evaluacion.append(12) #Quitar esto cuando empecemos a trabajar con la memoria. 
                else:
                    pila_evaluacion.append(valor)  
            elif isinstance(validaDeclaracion, bool) and not validaDeclaracion:
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
                    # else: 
                    #     if (isinstance(a, int)) or (isinstance(b, int)): 
                    #         if (isinstance(a, int)):
                    #             if not self.fnEncontrarTipo(b) in ['int', 'byte']:
                    #                 self.errores.append(['Error Semántico. Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ', 0, 1])
                    #                 return 'Null' 
                    #         if (isinstance(b, int)):
                    #             if not self.fnEncontrarTipo(a) in ['int', 'byte']:
                    #                 self.errores.append(['Error Semántico. Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ', 0, 1])
                    #                 return 'Null' 
                    #     else: 
                    #         if not self.fnEncontrarTipo(a) in ['int', 'byte'] or not self.fnEncontrarTipo(b) in ['int', 'byte'] :
                    #             self.errores.append(['Error Semántico. Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ', 0, 1])
                    #             return 'Null' 

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
                    #int y str
                    #int y bool
                    #str y int
                    #str y bool
                    #bool y int
                    #bool y str

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
                            # self.errores.append(['Error Semántico. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. ', 0, 1])
                            # return 'Null' 
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
                    # else: 
                    #     if (isinstance(a, bool)) or (isinstance(b, bool)): 
                    #         if (isinstance(a, bool)):
                    #             if self.fnEncontrarTipo(b) != 'boolean':
                    #                 self.errores.append(['Error Semántico. Las operaciones lógicas solo pueden ser realizadas entre tipos booleanos (boolean). ', 0, 1])
                    #                 return 'Null' 
                    #         if (isinstance(b, bool)):
                    #             if self.fnEncontrarTipo(a) != 'boolean':
                    #                 self.errores.append(['Error Semántico. Las operaciones lógicas solo pueden ser realizadas entre tipos booleanos (boolean). ', 0, 1])
                    #                 return 'Null'
                    #     else: 
                    #         if self.fnEncontrarTipo(a) != 'boolean' or self.fnEncontrarTipo(b) != 'boolean':
                    #             self.errores.append(['Error Semántico. Las operaciones lógicas solo pueden ser realizadas entre tipos booleanos (boolean). ', 0, 1])
                    #             return 'Null' 
                    #         else: #Después lo optimizo jaja
                    #             self.errores.append(['Error Semántico. Las operaciones lógicas solo pueden ser realizadas entre tipos booleanos (boolean). ', 0, 1])
                    #             return 'Null' 
                    
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
        #
        print('hola')
        ##
        # self.fnDeleteParametros()

#------Delete Parametros--------------------------------------------------------------------------------------
    def fnDeleteParametros(self):
        x = True
        con = 0
        while x :
            if 'Sin tipo'==self.ts[con][2]:
                self.ts.pop(con)
            else:
                con+=1
                if not con < len(self.ts):
                    x=False