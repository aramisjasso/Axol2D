import re

class Intermedio():
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
        self.pilaCodigo = []
        self.idIntruccion = 0

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
        # self.fnPrintTs()
        # if len(self.errores)!=0:
        #     self.compilo=False
        print('Inicio Código Intermedio')
        self.fnPrintPilaIntermedia()
        print('Fin Código Intermedio')
        #print(self.errores)

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
            for x,importa in enumerate (listaImportaciones):
                if importa == 'Background':
                    self.pilaCodigo.append([self.idIntruccion,('import','','Background')])
                    self.idIntruccion+=1
                elif importa == 'Players':
                    self.pilaCodigo.append([self.idIntruccion,('import','','Players')])
                    self.idIntruccion+=1


    #Parte de nivel
    def fnParteNivel(self):
        #Validación en TS del nombre de nivel
        #self.fnDeclararTipo(self.parteNivel[1],'Nivel')
        #self.fnBloqueDeclaracion()
        if not(self.parteMetodos is None):
            self.fnbloqueMetodos()
        if self.parteMetodoPrincipal[1] != 'Sin Método Axol': 
            self.fnMetodoPrincipal()


#----------Asignacion en TS de Estructura de Datos--------------------------------------
    def fnAsignar(self,valores,id,inMetodo = False, var = None,renin=None,axol=None, line=0 , lexpos=0 ):
        #Validar su declaración
        coma = False
        if axol == True and ',' in id:
            coma=True

        indice=self.fnIndice(id)
        tipo_id=self.ts[indice][2]
        if renin ==True:
            tipo_id =tipo_id[1]
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
            #Sacar tipo de valores
            
            #Validar si es arreglo, matriz o método
            if tipo_id[0]=='metodo':
                self.errores.append([f'Error Semántico (Línea {line}). El identificador {id} es de tipo método y no se puede asignar nigún valor.',line,lexpos])
                return
            elif tipo_id[0]=='arreglo':
                
                if tipo != tipo_id[0]:
                    
                    tipo=self.fnEncontrarTipo(valores[1][1])

                    if tipo[0] == tipo_id[0]:
                        if not tipo_id[1]in['obstacles', 'platform']:
                            if coma and tipo_id[1]=='int' and tipo==tipo_id:
                                #checar tamaño
                                indice = self.fnIndice(valores[1][1])
                                tamaño=int(self.ts[indice][3])
                                # print('String a todos',coma,id,tipo)
                                if tamaño!=2:
                                    self.errores.append([f'Error Semántico (Línea {line}). El último parametro al identificador [{id}] no corresponde al tamaño necesario',line,lexpos])
                            else:
                                self.errores.append([f'Error Semántico (Línea {line}). El identificador [{id}] es de tipo Arreglo y no se puede asignar otro Arreglo.',line,lexpos]) 
                        else:
                            if tipo != tipo_id:
                                self.errores.append([f'Error Semántico (Línea {line}). El parametro de start [{id}] no es correspodiente al tipo necesario [{tipo_id}].',line,lexpos]) 
                    else:
                        self.errores.append([f'Error Semántico (Línea {line}). El identificador [{id}] es de tipo Arreglo y no es valido el valor asignado.',line,lexpos])
                else:
                    #Validación por Tamaño
                    tamaño=int(valores[1])
                    tamaño_arreglo=int(self.ts[indice][3])
                    if tamaño_arreglo!=tamaño:
                        self.errores.append([f'Error Semántico (Línea {line}). La fila no se puede asignar al identificador {id} los tamaños no coinciden el tamaño declaro es: {tamaño_arreglo}',line,lexpos])
                        return 0
                    else:
                        if tipo_id[1]in['obstacles', 'platform']:
                            tamaño_errores = len(self.errores)
                            temp_valores=[]
                            #validar tipo
                            for x in range(tamaño):
                                temp_id = self.ts[indice+x*8+1][0]
                                temp_valores.append(self.ts[indice+x+1][3])
                                temp_valor = valores[2][x]
                                self.fnAsignar(temp_valor,temp_id, inMetodo,var,line=line,lexpos=lexpos)
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
                                if temp_valor[0]!='expresion':
                                    temp_valor=temp_valor[1]
                                # print('Asignar el arreglo:', temp_valor,temp_id,inMetodo,var,line,lexpos)
                                self.fnAsignar(temp_valor,temp_id,inMetodo,var,line=line,lexpos=lexpos)
                                #self.ts[indice+x+1][3]=valores[2][x]
                            if tamaño_errores != len(self.errores) or inMetodo:
                                for x in range(tamaño):
                                    self.ts[indice+x+1][3]=temp_valores[x]
                        

            else:
                #Validacion Tipos
                if tipo != tipo_id[0]:
                    
                    self.errores.append([f'Error Semántico (Línea {line}). El identificador {id} es de tipo Matriz y no es valido el valor asignado..',line,lexpos])
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
                        self.errores.append([f'Error Semántico (Línea {line}). La matriz tiene filas con diferentes tamaños',line,lexpos])
                    else:
                        #Los tamaños son diferentes
                        compara=False
                        if all( num == tamaño_matriz_y for num in lista_numero):
                            compara = True
                            
                        if tamaño_matriz_x !=tamaño_x or not compara:
                            self.errores.append([f'Error Semántico (Línea {line}). Las Matriz no se puede asignar al identificador {id} el tamaño declarado es de: {[tamaño_matriz_x,tamaño_matriz_y]}.',line,lexpos])
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
                                    self.fnAsignar(valor,temp_id,inMetodo,var,line=line,lexpos=lexpos)

                                    x1+=1
                                
                            #En caso de error
                            if tamaño_errores != len(self.errores) or inMetodo:
                                x1=0       
                                for x in range(tamaño_matriz_x):
                                    for y in range(tamaño_matriz_y):
                                        self.ts[indice+x1+1][3]=temp_valores[x1]
                                        x1+=1
                                 
        else:
            # tipo=self.fnRetornaValor(valores,tipo_id)
            # if renin:
                # print('Estoy evaluando return:',id,tipo_id,valores)

            if tipo_id in ['int', 'byte', 'boolean', 'char', 'string','obstacles', 'platform','background','character','player']:
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
                        self.errores.append([f'Error Semántico (Línea {line}). La fila no se puede asignar al identificador {id} de tipo de {tipo_id} solo se pueden asignar arreglos de tamaño: {tamaño_arreglo}',line,lexpos])
                    else:#Validación de inserción
                        tamaño_errores = len(self.errores)
                        temp_valores=[]
                        for x in range(tamaño):
                            temp_id = self.ts[indice+x+1][0]
                            temp_valores.append(self.ts[indice+x+1][3])
                            temp_valor = valores[2][x]
                            self.fnAsignar(temp_valor,temp_id,inMetodo,var,line=line,lexpos=lexpos)
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
                        self.errores.append([f'Error Semántico (Línea {line}). La fila no se puede asignar al identificador {id} de tipo de {tipo_id} solo se pueden asignar arreglos de tamaño: {tamaño_arreglo}',line,lexpos])
                    else:#Validación de inserción
                        tamaño_errores = len(self.errores)
                        temp_valores=[]
                        for x in range(tamaño):
                            temp_id = self.ts[indice+x+1][0]
                            temp_valores.append(self.ts[indice+x+1][3])
                            temp_valor = valores[2][x]
                            self.fnAsignar(temp_valor,temp_id,inMetodo,var,line=line,lexpos=lexpos)
                            #self.ts[indice+x+1][3]=valores[2][x]
                        if tamaño_errores != len(self.errores) or inMetodo:
                            for x in range(tamaño):
                                self.ts[indice+x+1][3]=temp_valores[x]
                        else:
                            self.ts[indice][3] = 'player'
                        

                # Asignación de una Expresión
                #print(valores)
                if valores[0] == 'expresion' and valores[1] != 'error':
                    #print(valores)
                    
                    self.postorden(valores)
                    #print(self.pila_semantica)
                    self.pilaCodigo.append([self.idIntruccion,('=',id,self.pila_semantica)])
                    self.idIntruccion+=1
                    valores = self.evaluar_pila(self.pila_semantica,var,line=line,lexpos=lexpos)
                    
                    #print(valores)
                    # self.ts[indice][3] = self.pila_semantica
                    self.pila_semantica = []

            
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
                # print('Declaración de método',x)
                metodo=x
                id = metodo[2]
                tipo= metodo[1]
                tipo=('metodo',tipo)
                parametros = metodo[3]
                line = metodo[5][0]
                lexpos = metodo[5][1]
                # print('linea y columna de metodo', line,lexpos)
                #Separación de Parametros
                self.fnSeparacionDeParametros(parametros[1])
                #Declaracion Métodos
                if self.listaParametros !='Error':
                    
                    contenido = metodo[4]
                    if contenido == 'Sin Contenido':
                        return
                    if len(contenido) == 4: 
                        instrucciones=contenido[1]
                        self.fnInstrucciones(instrucciones, id)
                        parteReturn=contenido[2]
                        line  = contenido[3][0]
                        lexpos =contenido[3][1]
                    else: 
                        parteReturn=contenido[1]
                        line  = contenido[2][0]
                        lexpos =contenido[2][1]
                    self.fnReturn(parteReturn,id,line=line,lexpos=lexpos)

                
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
                    # print('Checar parametros',parametros[0][1] )
                    if parametros[0][1][1] =='Sin Identificador':
                        self.listaParametros ='Error'
                        compara=False
                    parametros = parametros[1]
                    

                else:
                    self.listaParametros.append(parametros[1])
                    # print('Checar parametros',parametros[1] )
                    if parametros[1][1] =='Sin Identificador':
                        self.listaParametros ='Error'
                    compara = False
            else:
                    compara=False

#---------Procesado de instrucciones----------------------------------------------------
    def fnInstrucciones(self, instrucciones, llamada):
        # print('Instrucciones',instrucciones)
        lista_instrucciones=[]
        for x in range(len(instrucciones)):
            print('Instrucción chida2',instrucciones[x])
            instruccion=[instrucciones[x][1],instrucciones[x][2]]
            # print('Instrucciones',instruccion)
            lista_instrucciones.append(instruccion)
        
        #Se analizan todas las intrucciones para ver su tratamiento
        #print(lista_instrucciones)
        for x in lista_instrucciones:
            print('Instrucción chida',x)
            y=x[0]
            line = x[1][0]
            lexpos = x[1][1]
            #print(lista_instrucciones)

            if  y[0] == 'estructuraControl':
                
                if  y[1][0] == 'ifElse': 
                    condicion =  y[1][1]
                    #print(condicion)
                    if x[1][1][1] != 'error':
                      self.postorden(condicion)
                       #print(self.pila_semantica)
                      self.evaluar_pila(self.pila_semantica, llamada,line=line,lexpos=lexpos)
                    #condicionEvaluada = self.evaluar_pila(self.pila_semantica)
                      self.pila_semantica = []


                    #if con instrucciones sin else (o else sin instrucciones)
                    if len( y[1]) == 3: 
                        self.fnInstrucciones( y[1][2], llamada)
                    #Condición, instrucciones del if y else
                    elif len( y[1]) == 4: 
                        self.fnInstrucciones( y[1][2], llamada)
                        self.fnInstrucciones( y[1][3], llamada)
                    
                elif y[1][0] == 'switch':
                    #Validar que y[1][1] esté declarada
                    if not self.fnComprobarDeclaracion((y[1][1])):
                        self.errores.append([f'Error Semántico. La variable [{(y[1][1])}] no ha sido declarada.', line, lexpos])
                        return
                    #Validar que y[1][1] sea de tipo numérica
                    if not self.fnEncontrarTipo(y[1][1]) in ['int', 'byte']:
                        self.errores.append([f'Error Semántico. La estructura [switch] solo acepta variables numéricas como variable de control.', line, lexpos])
                        return
                    #Advertir si y[1][1] no ha sido inicializada
                    if self.fnRetornaValor(y[1][1]) == 'Null':
                        self.errores.append([f'Advertencia. La variable [{y[1][1]}] no ha sido inicializada, por lo tanto tomará el valor actual en memoria.', line, lexpos])
                    #print(y[1])
                # elif y[1][0] == 'for':
                #     print(y[1])
                elif y[1][0] == 'forEach':
                    #Validar que y[1][2] no esté declarada
                    if self.fnComprobarDeclaracion(y[1][2]):
                        self.errores.append([f'Error Semántico. La variable [{y[1][2]}] no puede ser utilizada como variable de control en la estructura [for each] porque ha sido declarada previamente. ', line, lexpos])
                        return
                    #Validar que y[1][3] sea una estructura de datos
                    if not self.fnComprobarDeclaracion(y[1][3]):
                        self.errores.append([f'Error Semántico. La estructura de datos [{y[1][3]}] no ha sido declarada. ', line, lexpos])
                        return
                    ed = self.fnEncontrarTipo(y[1][3])
                    if not (isinstance(ed, tuple) and ed[0] in ['arreglo', 'matriz']):
                        self.errores.append([f'Error Semántico. La variable [{y[1][3]}] no es una estructura de datos, por lo tanto no es posible recorrerla en la estructura de contol [for each]. ', line, lexpos])
                        return
                    #Validar que y[1][1] y y[1][3] sean del mismo tipo
                    if not y[1][1] == ed[1]:
                        self.errores.append([f'Error Semántico. La variable de control de tipo [{y[1][1]}] no coincide con el tipo de dato de la estructura de control de tipo {ed[1]}. ', line, lexpos])
                        return
                    
                    if len(y[1]) == 5:
                         self.fnInstrucciones(y[1][4], llamada)

                elif y[1][0] == 'while':
                    condicion = y[1][1]
                    self.postorden(condicion)
                    condEval = self.evaluar_pila(self.pila_semantica,llamada,line=line,lexpos=lexpos)
                    #print(condEval)
                    self.pila_semantica = []
                    #Evaluar instrucciones
                    if len(y[1]) == 3:
                         self.fnInstrucciones(y[1][2], llamada)
                elif y[1][0] == 'doWhile':
                    condicion = y[1][1]
                    self.postorden(condicion)
                    condEval = self.evaluar_pila(self.pila_semantica,llamada,line=line,lexpos=lexpos)
                    #print(condEval)
                    self.pila_semantica = []
                    #Evaluar instrucciones
                    if len(y[1]) == 3:
                        self.fnInstrucciones(y[1][2], llamada)

            elif y[0]=='expresionAsignacion':
                id=y[1][1]
                if id == 'Sin Identificador':
                    return

                if id !='error':
                    temp = self.fnComprobarDeclaracion(id)
                    #print('id:',id)
                    #print('Declaración antes', temp)
                    separado = id.split(',')
                    if ',' in id:
                        probar = separado[1]
                        try:
                            probar= float(probar)  # Intenta convertir a número
                        except (ValueError, TypeError):
                            ''''''
                    if ',' in id and isinstance(probar, str) :
                        id = separado[0]
                        #declaración
                        comprueba=self.fnComprobarDeclaracion(id)
                        if comprueba =='NoId' or comprueba == False:
                            self.errores.append([f'Error Semántico (Línea {line}. La variable [{id}] no ha sido declarada.', line,lexpos])
                        else:
                            #Validar que sea un arreglo 
                            tipo = self.fnEncontrarTipo(id)
                            if len(tipo) != 2 or tipo[0]=='Metodo':
                                self.errores.append([f'Error Semántico (Línea {line}. La variable [{id}] no ha puede tener acceso lineal.',line, lexpos])
                            else:
                                id2 = separado[1]
                                temp = self.fnComprobarDeclaracion(id2)
                                
                                if not temp or 'NoId'== temp:
                                #print('Declaración', temp)
                                    temp_id=id2
                                    id2=f'{llamada},{id2}'
                                    if 'NoId'== self.fnComprobarDeclaracion(id2):
                                        self.errores.append([f'Error Semántico (Línea {line}. La variable [{temp_id}] no ha sido declarada.',line, lexpos])
                                if 'int' != self.fnEncontrarTipo(id2):
                                    self.errores.append([f'Error Semántico (Línea {line}. La variable [{id2}] no es de tipo int.',line, lexpos])
                                else:
                                    if len(y)==3:
                                        id +=',0'
                                        valores= y[2]        
                                        if y[2][0] == 'llamadaMetodo':
                                            x2 = y[2]
                                            print('Aqui se hizo una llamada a Metodo' , y, 'valores',valores,id,True, llamada)
                                            self.fnLlamadaMetodo(x2[1],x2[2],x2[3],llamada,line=line,lexpos=lexpos)
                                            self.fnValidartipos(id,x2[1],True,line=line,lexpos=lexpos)
                                        else:
                                            self.fnAsignar(valores,id,True, llamada,line=line,lexpos=lexpos)
                                    elif len(y)==2:
                                        valores= y[1][2]
                                        self.fnAsignar(valores,id,True, llamada,line=line,lexpos=lexpos)
                    else:
                        if not temp or 'NoId'== temp:
                            #print('Declaración', temp)
                            temp_id=id
                            id=f'{llamada},{id}'
                            if 'NoId'== self.fnComprobarDeclaracion(id):
                                self.errores.append([f'Error Semántico (Línea {line}. La variable [{temp_id}] no ha sido declarada.',line, lexpos])
                        else:        
                            if len(y)==3:
                                valores= y[2]
                                
                                if y[2][0] == 'llamadaMetodo':
                                    x2 = y[2]
                                    print('Aqui se hizo una llamada a Metodo' , y, 'valores',valores,id,True, llamada)
                                    self.fnLlamadaMetodo(x2[1],x2[2],x2[3],llamada,line=line,lexpos=lexpos)
                                    self.fnValidartipos(id,x2[1],True,line=line,lexpos=lexpos)
                                else:
                                    self.fnAsignar(valores,id,True, llamada,line=line,lexpos=lexpos)
                            elif len(y)==2:
                                valores= y[1][2]
                                self.fnAsignar(valores,id,True, llamada,line=line,lexpos=lexpos)
                                
                    
            elif y[0]=='llamadaMetodo':
                id = y[1]
                cantidad = y[2]
                argumentos = y[3]
                #Separacion de métodos propios y axol
                if id in ['READ_BIN', 'READ_TEC','SAVE_BIN','PRINT', 'PRINT_CON', 'SHOW', 'POSITIONX','POSITIONY', 'RANDOM', 'GETPOSITION']:
                    print('Método Axol')
                else:
                    self.fnLlamadaMetodo(y[1],y[2],y[3],llamada,line=line,lexpos=lexpos)
            elif y[0] == 'llamadaStart':
                if llamada != 'axol':
                    self.errores.append([f'Error Semántico (Línea {line}. El método start() solo puede ser llamado desde el método principal axol2D play().',line, lexpos])
                    return
                # print(self.ts[0][0])
                # print(y[1])
                self.banderaStart = True
                if not (self.fnComprobarDeclaracion(y[1]) and self.fnEncontrarTipo(y[1]) == 'Nivel'):
                        nombreNivel = self.fnEncontrarMétodo()
                        self.errores.append([f'Error Semántico (Línea {line}. El identificador de llamada al método start() [{y[1]}] no coincide con el identificador del nivel [{nombreNivel}].',line, lexpos]) 
                else:
                    
                    self.pilaCodigo.append([self.idIntruccion,('call','start',(y[2][1][1],y[3][1][1],y[4][1][1],y[5][1][1],y[6][1][1],y[7][1][1]))])
                    return
                #print(y)
#----------Asignación Metodo ()--------------------------------------------------------------
    def fnLlamadaMetodo(self,id,cantidad,argumentos,id_desdellamado ,line = 0 , lexpos=0):
        print('Es una llamada de Metodo', id, cantidad, argumentos)
        #Validación si es un método
        tipo=self.fnEncontrarTipo(id)
        if not (isinstance(tipo, tuple) and tipo[0] in ['metodo']):
            self.errores.append([f'Error Semántico (Línea {line}). La variable llamada no es un método [{id}].', line, lexpos])
            return
        #Validar cantidad de argumentos
        indice=self.fnIndice(id)
        cantidad_metodo = int(self.ts[indice][3][0])
        # print('Catidad método: ',cantidad_metodo)
        if cantidad!=cantidad_metodo:
            self.errores.append([f'Error Semántico (Línea {line}). La cantidad de argumentos proporcionados, no corresponde con la cantidad de argumentos declarados.', line, lexpos])
            return
        #Validar tipo de argumento
        lista_argumentos=self.fnListaArgumentos(argumentos,cantidad)
        for x in range(cantidad_metodo):
            temp_id=self.ts[indice+x+1][0]
            #print('indice: ',temp_id)
            #print('valor: ', lista_argumentos[x])
            self.fnAsignar(lista_argumentos[x],temp_id,True,id_desdellamado,line=line,lexpos=lexpos)

        # print('Tipo',tipo[1])
        #lista_argumentos = fnSeparacionArgumentos(argumentos)

#---------Lista de Argumentos --------------------------------------------------------
    def fnListaArgumentos(self,argumentos,cantidad):
        lista_argumentos=[]
        for x in range(cantidad):
            lista_argumentos.append(argumentos[1])
            print('Checar Argumentos',argumentos[1])
            if x<=cantidad-1:
                argumentos=argumentos[2]
        return lista_argumentos

 #---------Procesado de intrucciones----------------------------------------------------
    def fnReturn(self,regreso,id,line=0,lexpos=0):
        # print('Return Metodo: ',id,regreso)
        #self.fnAsignar(regreso,id,True,id)
        # print('Retorno', regreso,id)
        self.fnAsignar(regreso,id,inMetodo = True, renin=True,line=line,lexpos=lexpos)#Porque el id nunca se puede llamar for

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

    def evaluar_pila(self, semantica,nameMetod =None,line=0,lexpos=0):

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
                if validaDeclaracion is False or validaDeclaracion == 'NoId':
                    elemento=temp_elemento
            validaDeclaracion =self.fnComprobarDeclaracion(elemento)
            if self.validaNumero(elemento):
                pila_evaluacion.append(int(elemento))
            #---Validación de Identificadores---

            elif isinstance(validaDeclaracion, bool) and validaDeclaracion:
                valor = self.fnRetornaValor(elemento)
                if valor == 'Null' and nameMetod is None:
                    self.errores.append([f'Advertencia (Línea {line}). La variable [{elemento}] no ha sido inicializada, por lo tanto tomará el valor actual en memoria.', line, lexpos])
                    pila_evaluacion.append(12) #Quitar esto cuando empecemos a trabajar con la memoria. 
                else:
                    pila_evaluacion.append(valor)  
            elif isinstance(validaDeclaracion, bool) and not validaDeclaracion:
                self.errores.append([f'Error Semántico (Línea {line}). La variable [{elemento}] no ha sido declarada.', line, lexpos])
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
                                self.errores.append([f'Error Semántico (Línea {line}). No se puede dividir entre cero.', line, lexpos])
                                return 'Null' 
                        elif elemento == '%':
                            if b != 0:
                                resultado = a % b
                            else:
                                self.errores.append([f'Error Semántico (Línea {line}). No se puede calcular el módulo de una división entre cero. ', line, lexpos])
                                return 'Null' 
                        pila_evaluacion.append(resultado) 
                    else: 
                        if (isinstance(a, int)) or (isinstance(b, int)): 
                            if (isinstance(a, int)):
                                if not self.fnEncontrarTipo(b) in ['int', 'byte']:
                                    self.errores.append([f'Error Semántico (Línea {line}).  Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ',line, lexpos])
                                    return 'Null' 
                            if (isinstance(b, int)):
                                if not self.fnEncontrarTipo(a) in ['int', 'byte']:
                                    self.errores.append([f'Error Semántico (Línea {line}). Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ',line, lexpos])
                                    return 'Null' 
                        else: 
                            if not self.fnEncontrarTipo(a) in ['int', 'byte'] or not self.fnEncontrarTipo(b) in ['int', 'byte'] :
                                self.errores.append([f'Error Semántico (Línea {line}).  Las operaciones aritméticas solo pueden ser realizadas entre tipos numéricos (int, byte). ',line, lexpos])
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
                        self.errores.append(['Error Semántico (Línea {line}. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. La condición no fue evaluada. ', line, lexpos])
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
        #print(self.parteMetodoPrincipal[1])
        self.fnInstrucciones(self.parteMetodoPrincipal[1], 'axol')
        
        
        # if self.banderaStart: 
        #     self.errores.append([f'Error Semántico (Línea {line}. Las operaciones relacionales solo pueden ser realizadas entre operandos del mismo tipo. La condición no fue evaluada. ', line, lexpos])

#----- Encontrar método Axol----------------------------------------------------------------------------------
    def fnEncontrarMétodo(self):
        for x in self.ts:
            if x[2]=='Nivel':
                return x[0]

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

#--fnValidarTipos----
    def fnValidartipos(self, id1, id2, metodo=False, line = 0, lexpos = 0):
        comprobar = self.fnComprobarDeclaracion(id1)
        #Se comprueba que estan declarados
        if comprobar == False or comprobar =='NoId':
             self.errores.append([f'Error Semántico (Línea {line}). [{id1}] No ha sido declarado. ', line , lexpos])
        else:
            comprobar = self.fnComprobarDeclaracion(id2)
            if comprobar == False or comprobar =='NoId':
                self.errores.append([f'Error Semántico (Línea {line}). [{id2}] No ha sido declarado. ', line , lexpos])
            else:#Se combrueban tipos:
                tipo1 = self.fnEncontrarTipo(id1)
                tipo1_antes = tipo1
                tipo2 = self.fnEncontrarTipo(id2)
                #print('Tipos',id1,id2, tipo1,tipo2)
                # si es un método
                if metodo == True:
                    tipo1 = ('metodo',tipo1)
                #print('Tipos',id1,id2, tipo1,tipo2)
                if tipo1 !=tipo2:
                    self.errores.append([f'Error Semántico (Línea {line}). [{id2}] No se puede asingar a [{id1}] de tipo [{tipo1_antes}]. ', line , lexpos])
    def fnPrintPilaIntermedia(self):
        for x in self.pilaCodigo:
            print(x)

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

# ------------ Encuentra el tipo de ts -------------------------------------------------------------
    def fnEncontrarTipo(self,id):
        for simbolo in self.ts:
            # [token[0].value, token[1],'Sin tipo', 'Sin Valor','Linea declación']
            if simbolo[0]==id:
                return simbolo[2]