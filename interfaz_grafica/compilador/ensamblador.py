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
        self.fnAcomodarNull()
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
        #self.fnImportaciones()
        self.fnStack_mas()
        self.fnData()
        self.fnCode()
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

    def fnStack_mas(self):
        self.codigo.append(f"""
.386
.model flat, stdcall
.stack 4096

include kernel32.inc
includelib kernel32.lib
include user32.inc
includelib user32.lib
                           
ExitProcess proto :dword
SetConsoleCursorPosition proto :dword, :dword
SetConsoleTextAttribute proto :dword, :dword
WriteConsole proto :dword, :dword, :dword, :dword, :dword
ReadConsole proto :dword, :dword, :dword, :dword, :dword
GetStdHandle proto :dword

_COORD struct
    _X sword ?
    _Y sword ?
_COORD ends""")
    #Acomoda código
    # def fnImportaciones(self):
    #     for importacion in self.importaciones:
    #         self.codigo.append(f"include {importacion[1][2]}")

#---------------------------------------------DATA-----------------------------------------------------------------
    def fnData(self):
        self.codigo.append(f"""
.data
    ; Constantes
    _VK_ESCAPE equ 1Bh              ; Código de la tecla ESC
    _VK_LEFT equ 25h                
    _VK_UP equ 26h
    _VK_RIGHT equ 27h         
    _VK_DOWN equ 28h
                           
    ; Variables para imprimir caracteres en pantalla   
    _pincel db ' ', 0
    _posicion _COORD <0, 0>    ; Posición inicial

    ; Manejadores de entrada y salida
    _stdoutHandle dd ?        ; Manejador de salida
    _stdinHandle dd ?         ; Manejador de entrada
                           
    ; Variables para WriteConsole
    _charsWritten dd ? ; Variable que recibe el total de caracteres escritos
                           
    ; Matriz de Colisiones
    _matriz_colision db 3600 dup (0) ; Matriz de 30 filas y 120 columnas llena de ceros
    ; Matriz de Colores
    _matriz_colores db 3600 dup(000h) ; Inicializa del color base del fondo
    ; Matriz de no vida
    _matriz_vida db 3600 dup (0)

    ; Matriz de posicion final
    _matriz_final db 3600 dup (0)
                           
""")
        self.fnTablaDeSimbolos()

    def fnTablaDeSimbolos(self):
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
                        valor += f"{simbolo[3]}"
                    else:
                        valor += f", {simbolo[3]}"
                identificador = f"\t{id} {tamaño} {valor}"
                
                identificador = f"\t{id} {tamaño} {valor}"
            elif tipo in ["string"]:
                valor = f"\"{simbolo[3]}\""
                identificador = f"\t{id} {tamaño} {valor}"
            else:
                valor = f"{simbolo[3]}"
                identificador = f"\t{id} {tamaño} {valor}"
            self.codigo.append(identificador)
            contador += 1
        self.codigo.append("""   
    _ren sword 0
    _col sword 0
    _vidas sword 0
    _ren_ini sword 0
    _col_ini sword 0
    _col_x dw 0
    _fil dw 0
    _cant_x dw 0
    _cant_y dw 0
    _color db 0
    _contador_y dw 0
    _contador_x dw 0
                           
    ; Mensajes
    _msjVictoria    db "   Enhorabuena   ", 0
    _msjDerrota     db "    Game Over    ", 0
    _msjArriba      db 17 dup (220), 0
    _msjAbajo       db 17 dup (223), 0
    ; Colores Fondo
    _colorCielo db 00h
    _colorSuelo db 00h
    _colorPersonaje db 00h""")

#---------------------------------------------------------------------------------CODE-------------------------------------------------------------------------------------- 

    def fnCode(self):
        self.codigo.append(".code")
        self.codigo.append("""_main proc
    ; Obtener manejador de salida
    invoke GetStdHandle, -11
    mov _stdoutHandle, eax

    """)
        self.fnAxol()
    
    # AXOL
    def fnAxol(self):
        
        # (Fila_pla, fila_obs ,Jugador, Fondo ,  elementos_fondo, Posión a llegar)
        self.axol.pop() #fin
        self.axol.pop() #start
        final = self.fnBuscar(self.axol.pop()[1][2])
        elementos_fondo = self.fnBuscar(self.axol.pop()[1][2])
        fondo = self.fnBuscar(self.axol.pop()[1][2])
        jugador = self.fnBuscar(self.axol.pop()[1][2])
        obstaculos = self.fnBuscar(self.axol.pop()[1][2])
        plataformas = self.fnBuscar(self.axol.pop()[1][2])
        
        tamaño_Code = len(self.axol)
        self.fnInstrucciones(self.axol,tamaño_Code)

        self.codigo.append("_inicializarColores:")
        background = fondo[3]
        if background == 'Forest':
            self.codigo.append('''  ; --- Bosque ---
    mov al, 033h
    mov _colorCielo, al
    mov al, 022h
    mov _colorSuelo, al''')
        elif background == 'Mountain':
            self.codigo.append('''  ; --- Montaña ---
    mov al, 033h
    mov _colorCielo, al
    mov al, 088h
    mov _colorSuelo, al''')
        elif background == 'Ocean':
            self.codigo.append('''    ; --- Oceano ---
    mov al, 033h
    mov _colorCielo, al
    mov al, 011h
    mov _colorSuelo, al
''')    
        elif background == 'Desert':
            self.codigo.append('''    ; --- Desierto ---
    mov al, 0EEh
    mov _colorCielo, al
    mov al, 066h
    mov _colorSuelo, al
''')
        elif background == 'City':
            self.codigo.append('''    ; --- Ciudad ---
    mov al, 033h
    mov _colorCielo, al
    mov al, 088h
    mov _colorSuelo, al
''')
        elif background == 'Village':
            self.codigo.append('''    ; --- Villa ---
    mov al, 033h
    mov _colorCielo, al
    mov al, 066h
    mov _colorSuelo, al
''')
        elif background == 'Cave':
            self.codigo.append('''    ; --- Cueva ---
    mov al, 000h
    mov _colorCielo, al
    mov al, 088h
    mov _colorSuelo, al
''')
        elif background == 'Swamp':
            self.codigo.append('''    ; --- Pantano ---
    mov al, 022h
    mov _colorCielo, al
    mov al, 066h
    mov _colorSuelo, al
''')
        elif background == 'River':
            self.codigo.append('''    ; --- Rio ---
    mov al, 0BBh
    mov _colorCielo, al
    mov al, 033h
    mov _colorSuelo, al
''')
        elif background == 'Island':
            self.codigo.append('''    ; --- Isla ---
    mov al, 0BBh
    mov _colorCielo, al
    mov al, 066h
    mov _colorSuelo, al
''')
        elif background == 'Castle':
            self.codigo.append('''    ; --- Castillo ---
    mov al, 077h
    mov _colorCielo, al
    mov al, 088h
    mov _colorSuelo, al
''')
        player = self.fnBuscar(f'{jugador[0]},3')[3]
        if player == 'wizard':
            self.codigo.append('''    ; Mago - Wizard
    mov al, 0DDh
    mov _colorPersonaje, al
''')
        elif player == 'archer':
            self.codigo.append('''    ; Arquero - Archer
    mov al, 0AAh
    mov _colorPersonaje, al
''')
        elif player == 'rogue':
            self.codigo.append('''    ; Pícaro - Rogue
    mov al, 0CCh
    mov _colorPersonaje, al
''')
        elif player == 'paladin':
            self.codigo.append('''    ; Paladín - Paladin 
    mov al, 0EEh
    mov _colorPersonaje, al
''')
        elif player == 'barbarian':
            self.codigo.append('''    ; Bárbaro - Barbarian
    mov al, 044h
    mov _colorPersonaje, al
''')
        elif player == 'assassin':
            self.codigo.append('''    ; Asesino - Assassin
    mov al, 077h
    mov _colorPersonaje, al
''')
        elif player == 'druid':
            self.codigo.append('''    ; Druida - Druid
    mov al, 022h
    mov _colorPersonaje, al
''')
        elif player == 'samurai':
            self.codigo.append('''    ; Samurai
    mov al, 011h
    mov _colorPersonaje, al
''')
        elif player == 'ninja':
            self.codigo.append('''    ; Ninja 
    mov al, 000h
    mov _colorPersonaje, al
''')
        elif player == 'priest':
            self.codigo.append('''    ; Sacerdote - Priest
    mov al, 0FFh
    mov _colorPersonaje, al
''')
        elif player == 'knight':
            self.codigo.append('''    ; Caballero - Knight
    mov al, 088h
    mov _colorPersonaje, al
''')

        #Final
        id = final[0]
        self.codigo.append("_fin_juego:")
        self.codigo.append(f""" ;posicion final para ganar
    xor eax, eax
    mov ax, {id}[2]
    imul eax, 120
    xor ebx, ebx
    mov bx, {id}[0]
    add ebx, eax
    mov byte ptr _matriz_final[ebx], 1
        """)
        #Fondo
        self.fnFondo(fondo[3])
        #jugador
        id =  jugador[0] 
        self.codigo.append("_inicio_jugador:")
        self.codigo.append(f""" ;posicion incial
    mov ax, {id}[4]
    mov _vidas, ax

    mov ax, {id}[0]
    mov _col_ini, ax
    mov _col, ax

    mov ax, {id}[2]
    mov _ren_ini, ax
    mov _ren, ax
        """)


        #elementos_fondo
        id =  elementos_fondo[0]
        tamaño = elementos_fondo[3]
        etiqueta = "elementos_fondo"
        self.fnBloques(id,tamaño, etiqueta, colision = False)

        
        #obstaculos
        id =  obstaculos[0]
        tamaño = obstaculos[3]
        etiqueta = "obstaculos"
        self.fnBloques(id, tamaño, etiqueta, quita_vida = True)

        #plataformas
        id =  plataformas[0]
        tamaño = plataformas[3]
        etiqueta = "plataformas"
        self.fnBloques(id, tamaño, etiqueta)

        self.codigo.append(""" 
_imprimirVidas: 
    mov word ptr [_posicion._X], 3    ; X = 0
    mov word ptr [_posicion._Y], 0   ; Y = 25

    ; Posiciona el cursor
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, 0AAh
    movzx ecx, _vidas         ; Número de caracteres a imprimir (2 en este caso)
    add ecx, ecx
    add ecx, ecx

; Ciclo para imprimir caracteres uno por uno
_loopVidas:
    push ecx                 ; Guarda el valor de ecx en la pila
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    pop ecx                  ; Restaura el valor de ecx
    loop _loopVidas
                           
; Esperar entrada del usuario
_tecla: 
    invoke GetAsyncKeyState, _VK_ESCAPE
    test eax, 8000h            ; Verificar si la tecla está presionada
    jnz _fin                    ; Salir si ESC está presionado

    invoke GetAsyncKeyState, _VK_LEFT
    test eax, 8000h            
    jnz _izquierda                

    invoke GetAsyncKeyState, _VK_RIGHT
    test eax, 8000h            
    jnz _derecha  

    invoke GetAsyncKeyState, _VK_UP
    test eax, 8000h            
    jnz _arriba  

    invoke GetAsyncKeyState, _VK_DOWN
    test eax, 8000h            
    jnz _abajo     

    ; Si no es una tecla especial, seguir leyendo
    jmp _tecla
    
_arriba:
    ; Calcula la posición destino 
    movzx eax, _ren
    dec eax
    imul eax, 120
    movzx ebx, _col
    add eax, ebx

    ; final
    movzx ebx, _matriz_final[eax] ; quitar vida
    cmp ebx, 1 
    je _gano                        

    ; vida menos
    movzx ebx, _matriz_vida[eax] ; quitar vida
    cmp ebx, 1 
    je _vida_menos
                                                     
    movzx ebx, _matriz_colision[eax] ; índice = ren_actual * 120 + col_actual
    ; Checa si el movimiento es permitido
    cmp ebx, 1         
    je _tecla                              

    ; Movimiento permitido
    call _borrar
    movzx eax, _ren          ; Cargar ren en eax con extensión cero
    cmp eax, 0              ; Comparar si ren es 0
    je _tecla                ; Saltar si lo es
    dec eax                 ; Decrementar ren
    mov _ren, ax             ; Guardar de vuelta en ren
    call _redibujar
    invoke Sleep, 150       ; 50 ms de pausa
    jmp _tecla

_abajo:
    ; Calcula la posición destino 
    movzx eax, _ren
    inc eax
    imul eax, 120
    movzx ebx, _col
    add eax, ebx

    ; final
    movzx ebx, _matriz_final[eax] ; quitar vida
    cmp ebx, 1 
    je _gano                        

    ; vida menos
    movzx ebx, _matriz_vida[eax] ; quitar vida
    cmp ebx, 1 
    je _vida_menos
                                                     
    movzx ebx, _matriz_colision[eax] ; índice = ren_actual * 120 + col_actual
    ; Checa si el movimiento es permitido
    cmp ebx, 1         
    je _tecla  
                           
    ; Movimiento permitido
    call _borrar
    movzx eax, _ren          ; Cargar ren en eax con extensión cero
    cmp eax, 29             ; Comparar si ren es 24
    je _tecla                ; Saltar si lo es
    inc eax                 ; Incrementar ren
    mov _ren, ax             ; Guardar de vuelta en ren
    call _redibujar
    invoke Sleep, 150 
    jmp _tecla

_izquierda:
    ; Calcula la posición destino 
    movzx eax, _ren
    imul eax, 120
    movzx ebx, _col
    dec ebx
    add eax, ebx

    ; final
    movzx ebx, _matriz_final[eax] ; quitar vida
    cmp ebx, 1 
    je _gano 
                                                              
    ; vida menos
    movzx ebx, _matriz_vida[eax] ; quitar vida
    cmp ebx, 1 
    je _vida_menos
                                                     
    movzx ebx, _matriz_colision[eax] ; índice = ren_actual * 120 + col_actual
    ; Checa si el movimiento es permitido
    cmp ebx, 1         
    je _tecla  
                          
    ; Movimiento permitido
    call _borrar
    movzx eax, _col          ; Cargar col en eax con extensión cero
    cmp eax, 0              ; Comparar si col es 0
    je _tecla                ; Saltar si lo es
    dec eax                 ; Decrementar col
    mov _col, ax             ; Guardar de vuelta en col
    call _redibujar
    invoke Sleep, 150 
    jmp _tecla

_derecha:
    ; Calcula la posición destino 
    movzx eax, _ren
    imul eax, 120
    movzx ebx, _col
    inc ebx
    add eax, ebx

    ; final
    movzx ebx, _matriz_final[eax] ; quitar vida
    cmp ebx, 1 
    je _gano                       

    ; vida menos
    movzx ebx, _matriz_vida[eax] ; quitar vida
    cmp ebx, 1 
    je _vida_menos
                                                     
    movzx ebx, _matriz_colision[eax] ; índice = ren_actual * 120 + col_actual
    ; Checa si el movimiento es permitido
    cmp ebx, 1         
    je _tecla  
                           
    ; Movimiento permitido
    call _borrar
    movzx eax, _col          ; Cargar col en eax con extensión cero
    cmp eax, 119            ; Comparar si col es 79
    je _tecla                ; Saltar si lo es
    inc eax                 ; Incrementar col
    mov _col, ax             ; Guardar de vuelta en col
    call _redibujar
    invoke Sleep, 150 
    jmp _tecla

_borrar:
    ; Calcular el índice
    movzx eax, _ren            ; renglón actual
    imul eax, 120           ; ren_actual * 120
    movzx ebx, _col
    add eax, ebx            ; índice = ren_actual * 120 + col_actual
    ; Cargar el valor de la matriz
    movzx ebx, byte ptr _matriz_colores[eax] ; Cargar color desde la matriz

    mov ax, _col
    mov word ptr [_posicion._X], ax
    mov ax, _ren
    mov word ptr [_posicion._Y], ax
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, ebx
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    ret

_redibujar:
    mov ax, _col
    mov word ptr [_posicion._X], ax
    mov ax, _ren
    mov word ptr [_posicion._Y], ax

    ; Posiciona el cursor
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    movzx eax, _colorPersonaje
    invoke SetConsoleTextAttribute, _stdoutHandle, eax
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    ret
    
_vida_menos:
    movzx eax, _vidas
    mov ebx, 4
    mul bx
    dec eax
    mov word ptr [_posicion._X], ax   
    mov word ptr [_posicion._Y], 0   

    ; Posiciona el cursor
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, 077h
    ; Guarda el valor de ecx en la pila
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0

    sub _vidas, 1
    ; Movimiento permitido
    call _borrar
    movzx eax, _col          ; Cargar col en eax con extensión cero
    cmp eax, 119            ; Comparar si col es 79
    je _tecla                ; Saltar si lo es
    inc eax                 ; Incrementar col
    mov _col, ax             ; Guardar de vuelta en col

    xor eax, eax
    mov ax, _vidas
    cmp ax, 0 
    je _gameover        
    
    mov ax, _col_ini
    mov _col, ax
    mov ax, _ren_ini
    mov _ren, ax
    call _redibujar
    invoke Sleep, 100

    jmp _tecla 
    ret
_gano:
    mov word ptr [_posicion._X], 50
    mov word ptr [_posicion._Y], 13 
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, 06Eh
    ; Guarda el valor de ecx en la pila
    invoke WriteConsole, _stdoutHandle, offset _msjArriba, 17, offset _charsWritten, 0
    mov word ptr [_posicion._X], 50
    mov word ptr [_posicion._Y], 14
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, 0E6h
    invoke WriteConsole, _stdoutHandle, offset _msjVictoria, 17, offset _charsWritten, 0
    mov word ptr [_posicion._X], 50
    mov word ptr [_posicion._Y], 15
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, 06Eh
    invoke WriteConsole, _stdoutHandle, offset _msjAbajo, 17, offset _charsWritten, 0
    invoke Sleep, 10000
    jmp _fin 
_gameover:
    mov word ptr [_posicion._X], 50
    mov word ptr [_posicion._Y], 13 
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, 08h
    ; Guarda el valor de ecx en la pila
    invoke WriteConsole, _stdoutHandle, offset _msjArriba, 17, offset _charsWritten, 0
    mov word ptr [_posicion._X], 50
    mov word ptr [_posicion._Y], 14
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, 80h
    invoke WriteConsole, _stdoutHandle, offset _msjDerrota, 17, offset _charsWritten, 0
    mov word ptr [_posicion._X], 50
    mov word ptr [_posicion._Y], 15
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax
    invoke SetConsoleTextAttribute, _stdoutHandle, 08h
    invoke WriteConsole, _stdoutHandle, offset _msjAbajo, 17, offset _charsWritten, 0
    invoke Sleep, 10000
    jmp fin                                 
_fin: 
    ; Salir del programa
    invoke ExitProcess, 0
_main endp

end _main""")
    
    # Fondo
    def fnFondo(self, valor):
        self.codigo.append("""; Posiciona el cursor
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax

    movzx eax, _colorCielo
    invoke SetConsoleTextAttribute, _stdoutHandle, eax

    ; Configuración inicial de variables
    mov ecx, 3000         ; Número de caracteres a imprimir (2 en este caso)

; Ciclo para imprimir caracteres uno por uno
_imprimirCielo:
    push ecx                 ; Guarda el valor de ecx en la pila
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    pop ecx                  ; Restaura el valor de ecx
    loop _imprimirCielo

    ;Color de Pasto en Matriz Color
    mov eax, 0          ; Número de la fila
    imul eax, 120        ; Calcula el índice inicial: ren * 120
    mov ebx, eax         ; Guarda el índice inicial en ebx

    mov ecx, 3000         ; Número de columnas en la fila (120)
_coloresCielo:
    movzx eax, _colorCielo
    mov byte ptr _matriz_colores[ebx], al 
    inc ebx                       ; Pasa a la siguiente celda
    loop _coloresCielo             ; Decrementa ecx y repite si no es 0

    mov word ptr [_posicion._X], 0    ; X = 0
    mov word ptr [_posicion._Y], 25   ; Y = 25

    ; Posiciona el cursor
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax

    movzx eax, _colorSuelo
    invoke SetConsoleTextAttribute, _stdoutHandle, eax

    ; Configuración inicial de variables
    mov ecx, 600         ; Número de caracteres a imprimir (2 en este caso)

; Ciclo para imprimir caracteres uno por uno
_imprimirPasto:
    push ecx                 ; Guarda el valor de ecx en la pila
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    pop ecx                  ; Restaura el valor de ecx
    loop _imprimirPasto

                           
    ;Color de Pasto en Matriz Color
    mov eax, 25          ; Número de la fila
    imul eax, 120        ; Calcula el índice inicial: ren * 120
    mov ebx, eax         ; Guarda el índice inicial en ebx

    mov ecx, 600         ; Número de columnas en la fila (120)
_coloresPasto:
    movzx eax, _colorSuelo
    mov byte ptr _matriz_colores[ebx], al
    inc ebx                       ; Pasa a la siguiente celda
    loop _coloresPasto             ; Decrementa ecx y repite si no es 0
   """)

    # Imprimir bloques 
    def fnBloques(self, id, tamaño, etiqueta, colision = True, quita_vida = False):
        id_mayusculas = etiqueta.upper()
        self.codigo.append(f"_{id_mayusculas}:")
        self.codigo.append(f"""\tmov esi, 0; Se carga en memoria el elemento""")
        self.codigo.append(f"\tmov _contador_x, {tamaño}; Cantidad de elementos de el arreglo")

        self.codigo.append(f"\n_MAIN_LOOP_{id_mayusculas}:")
        self.codigo.append(f""" ;Cargar cada bloque
        xor eax, eax 
        mov ax, {id}[esi] 
        mov _col_x, ax   
        add esi, 2

        xor eax, eax     
        mov ax, {id}[esi]     
        mov _fil, ax
        add esi, 2

        xor ax, ax
        mov ax, {id}[esi]
        mov _cant_x, ax
        add si, 2
        
        xor ax, ax
        mov ax, {id}[esi]
        mov _cant_y, ax
        add si, 2
        
        xor ax, ax
        mov ax, {id}[esi]
        mov _color, al
        add si, 2
                           
_{id_mayusculas}_LOOP_y:
        
    mov ax, _col_x
    mov word ptr [_posicion._X], ax   ; X = 0
    mov ax, _fil
    mov word ptr [_posicion._Y], ax   ; Y = 25

    ; Posiciona el cursor
    mov eax, _posicion
    invoke SetConsoleCursorPosition, _stdoutHandle, eax

    ; Modifica el color del caracter y el fondo
    mov al, _color
    invoke SetConsoleTextAttribute, _stdoutHandle, al

    ; Configuraci�n inicial de variables
    xor ecx, ecx

    mov cx, _cant_x       ; N�mero de caracteres a imprimir (2 en este caso)

_{id_mayusculas}_LOOP_PRINT_x:
    push ecx                 ; Guarda el valor de ecx en la pila
    invoke WriteConsole, _stdoutHandle, offset _pincel, 1, offset _charsWritten, 0
    pop ecx                  ; Restaura el valor de ecx
    loop _{id_mayusculas}_LOOP_PRINT_x

;Color de {id_mayusculas} en Matriz Color
    xor eax, eax
    mov ax, _fil          ; Número de la fila
    imul eax, 120        ; Calcula el índice inicial: ren * 120
    xor ebx, ebx
    mov bx, _col_x
    add eax, ebx
    mov ebx, eax         ; Guarda el índice inicial en ebx

    mov cx, _cant_x        ; Número de columnas en la fila (120)
_colores{id_mayusculas}:
    mov al, _color
    mov byte ptr _matriz_colores[ebx], al   ; Llena la celda actual con color
    """)
        if (colision):
            self.codigo.append(f"""  mov byte ptr _matriz_colision[ebx], 1   ; Llena la celda actual con 1""")
        if (quita_vida):
            self.codigo.append(f"""  mov byte ptr _matriz_vida[ebx], 1   ; Llena la celda actual con 1""")
        self.codigo.append(f"""    inc ebx                       ; Pasa a la siguiente celda
    loop _colores{id_mayusculas}             ; Decrementa ecx y repite si no es 0

    inc _fil
    sub _cant_y, 1
    mov cx, _cant_y
    cmp ecx, 0
    
    jnz _{id_mayusculas}_LOOP_y

;ciclo para resolver arreglo
    sub _contador_x, 1
    mov cx, _contador_x
    cmp ecx, 0
    jnz _MAIN_LOOP_{id_mayusculas}""")
        
    
    def fnInstrucciones(self, codigo, tamaño_Code):
        compara = True
        contador = 0
        while (compara):
            if tamaño_Code < contador + 1:
                compara = False
                break
            print("\tHola", codigo[contador])
            instruccion = codigo[contador][1]
            terceta = codigo[contador][0]
            signo = instruccion[0]
            operando_1 = instruccion[1]
            operando_2 = instruccion[2]
            es_id_1 =self.fnEsid(operando_1)
            es_id_2 =self.fnEsid(operando_2)
            pila_1 = self.fnEsTerceta(operando_1)
            pila_2 = self.fnEsTerceta(operando_2)
            self.codigo.append(f"_{terceta}:")
            if signo == "=":
                # Identifica el tamaño para asignar
                id =self.fnBuscar(instruccion[2].split("[")[0])
                if id[1] in [1, 50]:
                    tamaño = "BYTE"
                elif id [1] == 2 :
                    tamaño = "WORD"
                
                if es_id_1:
                    if tamaño =="WORD":
                        registro = "ax"
                    elif tamaño =="BYTE":
                        registro = "al"
                    self.codigo.append(f"\tmov {tamaño} ptr {registro}, {operando_1}")
                    operando_1 = registro
                #Si es una terceta
                elif pila_1:
                    if tamaño =="WORD":
                        registro = "ax"
                    elif tamaño =="BYTE":
                        registro = "al"
                    self.codigo.append(f"\tpop eax")
                    operando_1 = registro

                if pila_2:
                    registro2 = "ebx"
                    self.codigo.append(f"\tpop ebx")
                    id = operando_2.split("(")[0]
                    operando_2 = f"{id}{registro2}]"

                self.codigo.append(f"\tmov {tamaño} ptr {operando_2}, {operando_1}")


            elif signo in ["+", "-", "*", "/", "%"]:
                 
                if es_id_1: #Si es id
                    if tamaño =="WORD":
                        registro = "ax"
                    elif tamaño =="BYTE":
                        registro = "al"
                    self.codigo.append(f"\tmov {tamaño} ptr {registro}, {operando_1}")
                    operando_1 = registro
                elif pila_1: #Si es una terceta
                    self.codigo.append(f"\tpop eax")
                else: # Si es un número
                    self.codigo.append(f"\tmov eax, {operando_1}")

                #Segundo elemento
                if es_id_2: #Si es id
                    if tamaño =="WORD":
                        registro = "bx"
                    elif tamaño =="BYTE":
                        registro = "bl"
                    self.codigo.append(f"\tmov {tamaño} ptr {registro}, {operando_2}")
                    operando_2 = registro
                elif pila_2: #Si es una terceta
                    self.codigo.append(f"\tpop ebx")
                else:  # Si es un número
                    self.codigo.append(f"\tmov ebx, {operando_2}")
                
                if signo == "+":                
                    self.codigo.append(f"\tadd eax, ebx")
                elif signo == "-":
                    self.codigo.append(f"\tsub eax, ebx")
                elif signo == "*":
                    self.codigo.append(f"\tmul ebx")
                elif signo == "/":
                    self.codigo.append(f"\txor edx, edx")
                    self.codigo.append(f"\tdiv ebx")
                elif signo == "%":
                    self.codigo.append(f"\txor edx, edx")
                    self.codigo.append(f"\tdiv ebx")
                    self.codigo.append(f"\tmov eax, edx")
                self.codigo.append(f"\tpush eax ")

            elif signo in ["<", ">", "<=", ">=", "==", "!="]:
                if es_id_1: #Si es id
                    if tamaño =="WORD":
                        registro = "ax"
                    self.codigo.append(f"\tmov {tamaño} ptr {registro}, {operando_1}")
                    operando_1 = registro
                elif pila_1: #Si es una terceta
                    self.codigo.append(f"\tpop eax")
                else: # Si es un número
                    self.codigo.append(f"\tmov eax, {operando_1}")

                #Segundo elemento
                if es_id_2: #Si es id
                    if tamaño =="WORD":
                        registro = "bx"
                    self.codigo.append(f"\tmov {tamaño} ptr {registro}, {operando_2}")
                    operando_2 = registro
                elif pila_2: #Si es una terceta
                    self.codigo.append(f"\tpop ebx")
                else:  # Si es un número
                    self.codigo.append(f"\tmov ebx, {operando_2}")
                
                self.codigo.append(f"\tcmp eax, ebx") #Para hacer las comparaciones

                if signo == "<": #Si es menor
                    self.codigo.append("\tsetl bl")
                elif signo == "<=": #Si es menor o igual
                    self.codigo.append("\tsetle bl")
                elif signo == ">": #Si es mayor
                    self.codigo.append("\tsetg bl")
                elif signo == ">=": #Si es mayor o igual
                    self.codigo.append("\tsetge bl")
                elif signo == "==": #Si es igual
                    self.codigo.append("\tsete bl")
                elif signo == "!=": #Si es diferente
                    self.codigo.append("\tsetne bl")
                
                self.codigo.append("\txor eax, eax")
                self.codigo.append("\tmov al, bl")
                self.codigo.append(f"\tpush eax ")
            
            elif signo in ["&", "|"]:
                if es_id_1: #Si es id
                    if tamaño =="WORD":
                        registro = "ax"
                    self.codigo.append(f"\tmov {tamaño} ptr {registro}, {operando_1}")
                    operando_1 = registro
                elif pila_1: #Si es una terceta
                    self.codigo.append(f"\tpop eax")
                else: # Si es un número
                    self.codigo.append(f"\tmov eax, {operando_1}")

                #Segundo elemento
                if es_id_2: #Si es id
                    if tamaño =="WORD":
                        registro = "bx"
                    self.codigo.append(f"\tmov {tamaño} ptr {registro}, {operando_2}")
                    operando_2 = registro
                elif pila_2: #Si es una terceta
                    self.codigo.append(f"\tpop ebx")
                else:  # Si es un número
                    self.codigo.append(f"\tmov ebx, {operando_2}")

                if signo == "&": #Si es menor
                    self.codigo.append("\tand al, bl")
                elif signo == "|": #Si es menor o igual
                    self.codigo.append("\tor al, bl")
                
                self.codigo.append("\txor ebx, ebx")
                self.codigo.append("\tmov bl, al")
                self.codigo.append(f"\tpush ebx ")
                
            elif signo in ["IFF"]: #Si es falso
                if es_id_1: #Si es id
                    if tamaño =="WORD":
                        registro = "ax"
                    self.codigo.append(f"\tmov {tamaño} ptr {registro}, {operando_1}")
                    operando_1 = registro
                elif pila_1: #Si es una terceta
                    self.codigo.append(f"\tpop eax")
                else: # Si es un número
                    self.codigo.append(f"\tmov eax, {operando_1}")

                self.codigo.append(f"\tcmp eax, 0") #Para hacer la comparacion si es falso
                self.codigo.append(f"\tjz _{operando_2[1:-1]}") #Para hacer las comparaciones
            
            elif signo in ["GO TO"]: #Si es falso
                self.codigo.append(f"\tJMP _{operando_2[1:-1]}") #Para hacer las comparaciones
            self.codigo.append("") 
            #self.codigo.append(f"\t{self.axol[contador]}")
            contador += 1
        
        self.codigo.append(f"_{terceta+1}:")
    
    #Buscar id
    def fnBuscar(self, busca):
        for id in self.TS_Completa:
            if id[0] == busca:
                return id
        
    def fnEsid(self, busca):
        for id in self.TS_Completa:
            if id[0] == busca:
                return True
        return False
    
    def fnEsTerceta(self, valor):
        if "(" in valor:
            return True
        return False
    

    def fnAcomodarNull(self):
        for id in self.TS:
            if id[3] == "Null":
                id[3] = 0
       
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

