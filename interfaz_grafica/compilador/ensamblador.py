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
    def fnCorre(self,codigoIntermedio, TS, TS_Completa):
        self.codigoIntermedio = codigoIntermedio
        self.codigo = [] #Código a imprimir
        self.codigoConvertido = ""
        self.importaciones = []
        self.axol = []
        self.procedimientos = []
        self.TS = TS
        self.TS_Completa = TS_Completa
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
        self.fnAxol()
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

#---------------------------------------------DATA-----------------------------------------------------------------
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
                        y = 5
                        
                        for elemento_x in range(x):
                            valor = ""
                            contador += 1
                            for elemento_y in range(y):
                                contador += 1
                                simbolo = self.TS[contador]
                                if elemento_y == 0:
                                    valor += f"{simbolo[3]}"
                                else:
                                    valor += f", {simbolo[3]}"
                            if elemento_x == 0:
                                identificador = f"\t{id} {tamaño} {valor}"
                            else:
                                identificador += f"\n\t{tamaño} {valor}"
                    else:
                        for elemento in range(int(simbolo[3])):
                            contador += 1
                            simbolo = self.TS[contador]
                            if elemento == 0:
                                valor += f"{simbolo[3]}"
                            else:
                                valor += f", {simbolo[3]}"
                        
                        identificador = f"\t{id} {tamaño} {valor}"
                else:
                    x = int(simbolo[3][0])
                    y = int(simbolo[3][1])
                    
                    for elemento_x in range(x):
                        valor = ""
                        for elemento_y in range(y):
                            contador += 1
                            simbolo = self.TS[contador]
                            if elemento_y == 0:
                                valor += f"{simbolo[3]}"
                            else:
                                valor += f", {simbolo[3]}"
                        if elemento_x == 0:
                            identificador = f"\t{id} {tamaño} {valor}"
                        else:
                            identificador += f"\n\t{tamaño} {valor}"
                        
            elif tipo in ["obstacles", "platform"]:
                for elemento in range(5):
                    contador += 1
                    simbolo = self.TS[contador]
                    if elemento == 0:
                        valor += f"{simbolo[3]}"
                    else:
                        valor += f", {simbolo[3]}"
                
                identificador = f"\t{id} {tamaño} {valor}"
            
            elif tipo in ["player"]:
                for elemento in range(3):
                    contador += 1
                    simbolo = self.TS[contador]
                    if elemento == 0:
                        identificador = f"\t{id} {tamaño} {valor}"
                    else:
                        identificador += f"\n\t{tamaño} {valor}"
                
                identificador = f"\t{id} {tamaño} {valor}"
            elif tipo in ["string"]:
                valor = f"\"{simbolo[3]}\""
                identificador = f"\t{id} {tamaño} {valor}"
            else:
                valor = f"{simbolo[3]}"
                identificador = f"\t{id} {tamaño} {valor}"
            self.codigo.append(identificador)
            contador += 1
        self.codigo.append("""        _col db 0
        _fil db 0
        _cant_x dw 0
        _cant_y dw 0
        _color db 0""")

#---------------------------------------------------------------------------------CODE-------------------------------------------------------------------------------------- 
    def fnAxol(self):
        self.codigo.append(".CODE")
        self.codigo.append("""        MOV AX,@DATA
        MOV DS,AX
""")
        compara = True
        contador = 0
        
        # (Fila_pla, fila_obs ,Jugador, Fondo ,  elementos_fondo, Posión a llegar)
        self.axol.pop() #fin
        self.axol.pop() #start
        final = self.fnBuscar(self.axol.pop()[1][2])
        elementos_fondo = self.fnBuscar(self.axol.pop()[1][2])
        fondo = self.fnBuscar(self.axol.pop()[1][2])
        jugador = self.fnBuscar(self.axol.pop()[1][2])
        obstaculos = self.fnBuscar(self.axol.pop()[1][2])
        plataformas = self.fnBuscar(self.axol.pop()[1][2])
        
        # tamaño_Code = len(self.axol)
        # while (compara):
        #     if tamaño_Code < contador + 1:
        #         compara = False
        #         break
        #     self.codigo.append(f"\t{self.axol[contador]}")
        #     contador += 1

        #elementos_fondo
        id =  elementos_fondo[0]
        tamaño = elementos_fondo[3]
        etiqueta = "elementos_fondo"
        self.fnBloques(id,tamaño, etiqueta)

        #plataformas
        id =  plataformas[0]
        tamaño = plataformas[3]
        etiqueta = "plataformas"
        self.fnBloques(id, tamaño, etiqueta)
       
            
        #obstaculos
        id =  obstaculos[0]
        tamaño = obstaculos[3]
        etiqueta = "obstaculos"
        self.fnBloques(id, tamaño, etiqueta)


    # Imprimir bloques 
    def fnBloques(self, id, tamaño, etiqueta):
        id_mayusculas = etiqueta.upper()
        self.codigo.append(f"{id_mayusculas}:")
        self.codigo.append(f"\tmov si, 0; Se carga en memoria el elemento")
        self.codigo.append(f"\tmov cx, {tamaño}; Cantidad de elementos de el arreglo")

        self.codigo.append(f"\nMAIN_LOOP_{id_mayusculas}:")
        self.codigo.append(f"""          push cx ; contador arreglo        
        xor ax, ax
        mov ax, {id}[si]
        mov _col, al
        add si, 2
                           
        xor ax, ax
        mov ax, {id}[si]
        mov _fil, al
        add si, 2

        xor ax, ax
        mov ax, {id}[si]
        mov _cant_x, ax
        add si, 2
        
        xor ax, ax
        mov ax, {id}[si]
        mov _cant_y, ax
        add si, 2
        
        xor ax, ax
        mov ax, {id}[si]
        mov _color, al
        add si, 2
        
        mov cx, _cant_y
{id_mayusculas}_LOOP:
        
        push cx ; Guardar cantidad y
                           
        mov ah, 02h       ; Función para mover el cursor
        mov bh, 0         ; Página de video
        mov dl, _col         ; Columna (posición X)
        mov dh, _fil         ; Fila (posición Y)

        int 10h           ; Llamada a BIOS para posicionar el cursor

        mov ah, 09h       ; Función para escribir carácter con atributo
        mov al, ' '       ; Carácter a imprimir
        mov bl, _color       ; Atributo de color (fondo negro, texto blanco brillante)
        mov cx, _cant_x        ; Cantidad de veces que se imprime
        int 10h           ; Llamada a BIOS para imprimir
        
        inc _fil
        pop cx
        loop {id_mayusculas}_LOOP

        pop cx                   
        loop MAIN_LOOP_{id_mayusculas}""")
    #Buscar id
    def fnBuscar(self, busca):
        for id in self.TS_Completa:
            if id[0] == busca:
                return id
        

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
