import ply.yacc as yacc
import compilador.lexico as le
class Sintactico():
    def __init__(self):
        #tokens
        self.tokens = le.tokens
        # Orden de Procedencia
        # Orden de Procedencia
        self.precedence = (
            ('left', 'MAS', 'MENOS'),
            ('left', 'MAS_MAS', 'MENOS_MENOS'),
            ('left', 'POR', 'DIVISION', 'MODULO')
        )

        #Lista de errores
        self.errores = []
        self.parser = None
    
    def build(self):
        self.parser = yacc.yacc(module=self,method='LALR', debug=True)
        #parser = yacc.yacc(debug=True, write_tables=True, outputdir='.')




    #------------------------------------------ P R O G R A M A ---------------------------------------------------
    #<programa> ::= <importaciones> <clases> <nivel>
    def p_programa(self,p):
        '''programa : importaciones nivel
                    | importaciones
                    | nivel
                    | empty
                    
                    
                    | bloqueDeclaracion 
                    | expresion'''
        if(len(p) == 2):
            p[0] = p[1]
        else:
            p[0] = ('programa', p[1], p[2])
    #----------------------------------------------------------------------------------------------------------

    #-------------------------------------- I M P O R T A C I O N E S ---------------------------------------------
    #<importaciones> ::= <importacion> <restoImportaciones>
    def p_importaciones(self,p):
        '''importaciones : importacion restoImportaciones'''
        p[0] = [p[1]] + p[2]  # Concatenamos la importación actual con las importaciones restantes

    #<restoImportaciones> ::= <importacion> <restoImportaciones> | ε
    def p_restoImportaciones(self,p):
        '''restoImportaciones : importacion restoImportaciones
                            | empty'''
        if len(p) == 3:  # Hay una importación seguida de más importaciones
            p[0] = [p[1]] + p[2]  # Concatenamos la importación actual con las importaciones restantes
        else:  # No hay más importaciones
            p[0] = []  # Lista vacía

    #<importacion> ::= import <libreriaAxol> ;
    def p_importacion(self,p):
        '''importacion : IMPORT libreriaAxol PUNTO_Y_COMA'''
        p[0] = p[1]

    #<libreriaAxol> ::= Controllers | Enemies
    def p_libreriaAxol(self,p):
        '''libreriaAxol : CONTROLLERS
                        | ENEMIES'''
        p[0] = p[1]
    #----------------------------------------------------------------------------------------------------------

    #-------------------------------------------- N I V E L ---------------------------------------------------
    #<nivel> ::= level identificador { <contenidoNivel> } | ε
    def p_nivel(self,p):
        '''nivel : LEVEL IDENTIFICADOR LLAVE_ABRE contenidoNivel LLAVE_CIERRA'''
        if len(p) == 6:
            p[0] = ('nivel', p[4])

    #<contenidoNivel> ::= <atributos> <metodos> <metodoPrincipal>
    def p_contenidoNivel(self,p):
        '''contenidoNivel : bloqueDeclaracion bloqueMetodos metodoPrincipal'''
        p[0] = ('contenidoNivel', p[1], p[2], p[3])

    #<metodoPrincipal> ::= axol2D play ( ) { <instrucciones>  identificador.start(); }
    def p_metodoPrincipal(self,p):
        '''metodoPrincipal : AXOL2D PLAY PARENTESIS_ABRE PARENTESIS_CIERRA LLAVE_ABRE instrucciones LLAVE_CIERRA'''
        p[0] = ('metodoPrincipal', p[6], p[7])

    def p_llamadaStart(self,p):
        '''llamadaStart : IDENTIFICADOR PUNTO START PARENTESIS_ABRE PARENTESIS_CIERRA PUNTO_Y_COMA'''
        p[0] = ('llamadaStart', p[1])
    #----------------------------------------------------------------------------------------------------------

    #-------------------------------- B L O Q U E   D E   D E C L A R A C I O N  ------------------------------
    #<bloqueDeclaracion> ::= <declaracion> <restoDeclaracion>
    def p_bloqueDeclaracion(self,p):
        '''bloqueDeclaracion : declaracion restoDeclaracion'''
        p[0] = ('bloqueDeclaracion', p[1], p[2])

    #<restoDeclaracion> ::= <declaracion> <restoDeclaracion> | ε
    def p_restoDeclaracion(self,p):
        '''restoDeclaracion : declaracion restoDeclaracion
                            | empty'''
        if len(p) == 3:
            p[0] = ('restoDeclaracion', p[1], p[2])
        else:
            p[0] = None

    #<declaracion> ::= ( <declaracionTipo> ( <valorDeclaracion> | ε ) ; ) | <declaracionEstructuraDatos>
    def p_declaracion(self,p):
        '''declaracion : declaracionTipo PUNTO_Y_COMA
                    | declaracionTipo valorDeclaracion PUNTO_Y_COMA
                    | declaracionEstructuraDatos '''
        # Declaracion Simple
        if len(p) == 3:
            p[0] = ('declaracion', p[1])
        # Declaracion con Asignacion
        elif len(p) == 4:
            p[0] = ('declaracion', p[1], p[2])
        # Declaracion de Estructura de Datos
        else: 
            p[0] = ('declaracionEstructuraDatos', p[1])

    #<declaracionTipo> ::= <tipoDato> idenfiticador
    def p_declaracionTipo(self,p):
        '''declaracionTipo : tipoDato IDENTIFICADOR'''
        p[0] = ('declaracionTipo', p[1], p[2])

    #<valorDeclaracion> ::= = ( <expresion> | <booleano> | <llamadaMetodo>
    def p_valorDeclaracion(self,p):
        '''valorDeclaracion : IGUAL expresion
                            | IGUAL booleano
                            | IGUAL llamadaMetodo
                            | IGUAL VALOR_CHAR
                            | IGUAL VALOR_STRING'''
        p[0] = p[2]

    #<tipoDato> ::= int | string | boolean | char | byte 
    def p_tipoDato(self,p):
        '''tipoDato : INT
                    | STRING
                    | BOOLEANO
                    | CHAR
                    | BYTE'''
        p[0] = p[1]
    #----------------------------------------------------------------------------------------------------------

    #----------------------------------- B L O Q U E   D E   M E T O D O S  -----------------------------------
    #<bloqueMetodos> ::= <metodoDeclaracion> <restoMetodos> | ε
    def p_bloqueMetodos(self,p):
        '''bloqueMetodos : metodoDeclaracion restoMetodos'''
        p[0] = ('bloqueMetodos', p[1], p[2])

    #<restoMetodos> ::= <metodosDeclaracion> | ε
    def p_restoMetodos(self,p):
        '''restoMetodos : bloqueMetodos restoMetodos
                        | empty'''
        if len(p) == 3:
            p[0] = ('restoMetodos', p[1], p[2])
        else:
            p[0] = p[1]

    #<metodoDeclaracion> ::= method <tipoDato> identificador ( <parametros> ) { <contenidoMetodo> }
    def p_metodoDeclaracion(self,p):
        '''metodoDeclaracion : METHOD tipoDato IDENTIFICADOR PARENTESIS_ABRE parametros PARENTESIS_CIERRA LLAVE_ABRE contenidoMetodo LLAVE_CIERRA'''
        p[0] = ('metodoDeclaracion', p[2], p[5], p[8])

    #<contenidoMetodo> ::= <instrucciones> return <expresion> ;
    def p_contenidoMetodo(self,p):
        '''contenidoMetodo : instrucciones RETURN expresion PUNTO_Y_COMA'''
        p[0] = ('contenidoMetodo', p[1], p[3])

    #<parametros> ::= <tipoDato> identificador |
    #                 <tipoDato> identificador , <parametros> | 
    #                 ε
    def p_parametros(self,p):
        '''parametros : tipoDato IDENTIFICADOR
                    | tipoDato IDENTIFICADOR COMA parametros
                    | empty'''
        if len(p) == 3:
            p[0] = ('parametros', p[1], p[2])
        elif len(p) == 5:
            p[0] = ('parametros', p[1], p[2], p[4])
        else:
            p[0] = None
    #----------------------------------------------------------------------------------------------------------

    #---------------------------------------- I N S T R U C C I O N E S ---------------------------------------
    #<instruccionesNivel> ::= 
    # def p_instruccionesNivel(self,p):
    #     '''instruccionesNivel : instrucciones llamadaStart'''
    #     p[0] = ('instruccionesNivel', p[1], p[2])

    #<instrucciones> ::= <instruccion> <instrucciones>
    def p_instrucciones(self,p):
        '''instrucciones : instruccion
                        | instruccion instrucciones'''
        if len(p) == 2:
            p[0] = [p[1]]  # Lista con una instrucción
        else:
            p[0] = [p[1]] + p[2]  # Concatenar las instrucciones

    #<instruccion> ::=  ( <expresionAsignacion> | (<llamadaMetodo>) ; | <estructuraControl>
    def p_instruccion(self,p):
        '''instruccion : expresionAsignacion PUNTO_Y_COMA
                    | llamadaMetodo PUNTO_Y_COMA
                    | estructuraControl
                    | expresion PUNTO_Y_COMA
                    | llamadaStart'''
        p[0] = ('instruccion', p[1])
    #----------------------------------------------------------------------------------------------------------

    #------------------------------ E S T R U C T U R A S   D E   C O N T R O L -------------------------------
    #<estructuraControl> ::= <ifElse> | <switch> | <for> | <forEach> | <while> | <doWhile> 
    def p_estructuraControl(self,p):
        '''estructuraControl : ifElse
                            | switch
                            | for
                            | forEach
                            | while
                            | doWhile'''
        p[0] = ('estructuraControl', p[1])

    #<ifElse> ::= if ( <condicion> ) { <instrucciones> } | if ( <condicion> ) { <instrucciones> } else { <instrucciones> } 
    def p_ifElse(self,p):
        '''ifElse : IF expresion LLAVE_ABRE instrucciones LLAVE_CIERRA
                | IF expresion LLAVE_ABRE instrucciones LLAVE_CIERRA ELSE LLAVE_ABRE instrucciones LLAVE_CIERRA'''
        if len(p) == 6:
            p[0] = ('ifElse', p[2], p[4])
        else:
            p[0] = ('ifElse', p[2], p[4], p[8])

    #<switch> ::= switch ( identificador ) { <casos> }
    def p_switch(self,p):
        '''switch : SWITCH expresion LLAVE_ABRE casos LLAVE_CIERRA'''
        p[0] = ('switch', p[2], p[4])

    #<casos> ::= <caso> <restoCasos>
    def p_casos(self,p):
        '''casos : caso restoCasos'''
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = ('casos', p[1], p[2])

    #<caso> ::= case numero : <instrucciones> break ;
    def p_caso(self,p):
        '''caso : CASE NUMERO DOS_PUNTOS instrucciones BREAK PUNTO_Y_COMA'''
        p[0] = ('caso', p[4])

    #<restoCasos> ::= <casos> | default : <instrucciones> }
    def p_restoCasos(self,p):
        '''restoCasos : casos
                    | DEFAULT DOS_PUNTOS instrucciones'''
        if len(p) == 2:  #casos
            p[0] = p[1]
        else:  #default
            p[0] = ('default', p[3])

    #<for> ::= for ( int identificador ; <condicion> ;  <expresionAsignacion> ) { <instrucciones> }
    def p_for(self,p):
        '''for : FOR PARENTESIS_ABRE INT IDENTIFICADOR IGUAL NUMERO PUNTO_Y_COMA expresionComparacion PUNTO_Y_COMA expresionAsignacion PARENTESIS_CIERRA LLAVE_ABRE instrucciones LLAVE_CIERRA'''
        p[0] = ('for', p[8], p[10], p[13])

    #<forEach> ::= for ( <tipoDato> identificador : identificador ) { <instrucciones> }
    def p_forEach(self,p):
        '''forEach : FOR PARENTESIS_ABRE tipoDato IDENTIFICADOR DOS_PUNTOS IDENTIFICADOR PARENTESIS_CIERRA LLAVE_ABRE instrucciones LLAVE_CIERRA'''
        p[0] = ('forEach', p[3], p[4], p[6], p[9])

    #<while> ::= while ( <condicion> ) { <instrucciones> }
    def p_while(self,p):
        '''while : WHILE PARENTESIS_ABRE expresion PARENTESIS_CIERRA LLAVE_ABRE instrucciones LLAVE_CIERRA'''
        p[0] = ('while', p[3], p[6])

    #<doWhile> ::= do while ( <condicion> ) { <instrucciones> } 
    def p_doWhile(self,p):
        '''doWhile : DOWHILE PARENTESIS_ABRE expresion PARENTESIS_CIERRA LLAVE_ABRE instrucciones LLAVE_CIERRA'''
        p[0] = ('doWhile', p[4], p[7])
    #----------------------------------------------------------------------------------------------------------

    #-------------------------------------- E X P R E S I O N -------------------------------------------------
    #<expresion> ::= <expresionAritmetica> | <expresionLogica> | <expresionPostfijo> | <expresionParentesis>
    def p_expresion(self,p):
        '''expresion : expresionAritmetica
                    | expresionLogica
                    | expresionUnaria
                    | expresionParentesis'''
        p[0] = ('expresion', p[1])

    #<expresionAritmetica> ::= <termino> <restoExpresionAritmetica>
    def p_expresionAritmetica(self,p):
        '''expresionAritmetica : termino restoExpresionAritmetica'''
        if p[2] is None:
            p[0] = p[1]
        else:
            p[0] = ('expresionAritmetica', p[1], p[2])

    #<restoExpresionAritmetica> ::= <operadorAdicion> <termino> <restoExpresionAritmetica> | ε
    def p_restoExpresionAritmetica(self,p):
        '''restoExpresionAritmetica : operadorAdicion termino restoExpresionAritmetica
                                    | empty'''
        if len(p) == 2:
            p[0] = None  # ε
        elif p[3] is None:
            p[0] = ('restoExpresionAritmetica', p[1], p[2])
        else:
            p[0] = ('restoExpresionAritmetica', p[1], p[2], p[3])

    #<termino> ::= <factor> <restoTermino>
    def p_termino(self,p):
        '''termino : factor restoTermino'''
        if p[2] is None:
            p[0] = p[1]
        else:
            p[0] = ('termino', p[1], p[2])

    #<restoTermino> ::= <operadorMultiplicacion> <factor> <restoTermino> | ε
    def p_restoTermino(self,p):
        '''restoTermino : operadorMultiplicacion factor restoTermino
                        | empty'''
        if len(p) == 2:
            p[0] = None  # ε
        elif p[3] is None:
            p[0] = ('restoTermino', p[1], p[2])
        else:
            p[0] = ('restoTermino', p[1], p[2], p[3])

    #<factor> ::= IDENTIFICADOR | NUMERO
    def p_factor(self,p):
        '''factor : IDENTIFICADOR
                | NUMERO
                | expresionParentesis'''
        p[0] = ('factor', p[1])

    #<operadorAdicion> ::= MAS | MENOS
    def p_operadorAdicion(self,p):
        '''operadorAdicion : MAS
                        | MENOS'''
        p[0] = p[1]

    #<operadorMultiplicacion> ::= POR | DIVISION | MODULO
    def p_operadorMultiplicacion(self,p):
        '''operadorMultiplicacion : POR
                                | DIVISION
                                | MODULO'''
        p[0] = p[1]

    #<expresionUnaria> ::= <operadorUnario> <factor>
    def p_expresionUnaria(self,p):
        '''expresionUnaria : operadorUnario factor'''
        p[0] = ('expresionUnaria', p[1], p[2])

    #<operadorUnario> ::= <operadorAdicion> | NOT
    def p_operadorUnario(self,p):
        '''operadorUnario : operadorAdicion
                        | NOT'''
        p[0] = p[1]

    #<expresionParentesis> ::= ( <expresion> )
    def p_expresionParentesis(self,p):
        '''expresionParentesis : PARENTESIS_ABRE expresion PARENTESIS_CIERRA'''
        p[0] = ('expresionParentesis', p[2])

    # Producción para <expresionLogica>
    def p_expresionLogica(self,p):
        '''expresionLogica : expresionLogicaConjuncion restoExpresionLogica'''
        if p[2] is None:
            p[0] = p[1]
        else:
            p[0] = ('expresionLogica', p[1], p[2])

    # Producción para <restoExpresionLogica>
    def p_restoExpresionLogica(self,p):
        '''restoExpresionLogica : operadorLogico expresionLogicaConjuncion restoExpresionLogica
                                | empty'''
        if len(p) == 2:  # ε (vacio)
            p[0] = None
        else:
            p[0] = ('restoExpresionLogica', p[1], p[2], p[3])

    # Producción para <expresionLogicaConjuncion>
    def p_expresionLogicaConjuncion(self,p):
        '''expresionLogicaConjuncion : expresionComparacion restoExpresionComparacion'''
        if p[2] is None:
            p[0] = p[1]
        else:
            p[0] = ('expresionLogicaConjuncion', p[1], p[2])

    # Producción para <restoExpresionComparacion>
    def p_restoExpresionComparacion(self,p):
        '''restoExpresionComparacion : operadorComparacion expresionComparacion
                                    | empty'''
        if len(p) == 2:  # ε (vacio)
            p[0] = None
        else:
            p[0] = ('restoExpresionComparacion', p[1], p[2])

    # Producción para <expresionComparacion>
    def p_expresionComparacion(self,p):
        '''expresionComparacion : expresionAritmetica operadorComparacion expresionAritmetica'''
        p[0] = ('expresionComparacion', p[1], p[2], p[3])

    # Producción para <operadorComparacion>
    def p_operadorComparacion(self,p):
        '''operadorComparacion : DOBLE_IGUAL
                            | DIFERENTE
                            | MENOR_QUE
                            | MENOR_IGUAL_QUE
                            | MAYOR_QUE
                            | MAYOR_IGUAL_QUE'''
        p[0] = p[1]

    # Producción para <operadorLogico>
    def p_operadorLogico(self,p):
        '''operadorLogico : AND
                        | OR'''
        p[0] = p[1]

    #<expresionPostfijo> ::= identificador <operadorPostfijo> |
    #                        this . <identificador> <operadorPostfijo>
    def p_expresionPostfijo(self,p):
        '''expresionPostfijo : IDENTIFICADOR operadorPostfijo
                            | THIS PUNTO IDENTIFICADOR operadorPostfijo'''
        if len(p) == 3:
            p[0] = ('expresionPostfijo', p[1], p[2])  # identificador operadorPostfijo
        else:
            p[0] = ('expresionPostfijoThis', p[3], p[4])  # this.identificador operadorPostfijo

    #<operadorPostfijo> ::= ++ | ––
    def p_operadorPostfijo(self,p):
        '''operadorPostfijo : MAS_MAS
                            | MENOS_MENOS'''
        p[0] = p[1]
    #----------------------------------------------------------------------------------------------------------

    #---------------------------- E X P R E S I O N   D E   A S I G N A C I O N -------------------------------
    # 
    def p_izqAsignacion(self,p):
        '''izqAsignacion : IDENTIFICADOR operadorAsignacion
                        | THIS PUNTO IDENTIFICADOR operadorAsignacion
                        | accesoLineal operadorAsignacion
                        | accesoMatriz operadorAsignacion'''
        if len(p) == 3 and p[1] == 'IDENTIFICADOR':
            p[0] = ('izqAsignacion', p[2])
        elif len(p) == 5:
            p[0] = ('izqAsignacion', p[3], p[4])
        else:
            p[0] = ('izqAsignacion', p[1], p[2])

    #<expresionAsignacion> ::= <identificador> <operadorAsignacion> <expresion> |
    #                          <identificador> = (<llamadaMetodo>  | <definicionArreglo>)
    #                          <identificador> = <expresionPostfijo> |
    #                          this . <identificador> <operadorAsignacion> <expresion>  | 
    #                          <clase> identificador = <objeto>
    def p_expresionAsignacion(self,p):
        '''expresionAsignacion : izqAsignacion expresion
                            | izqAsignacion llamadaMetodo
                            | izqAsignacion objeto
                            | definicionArreglo
                            | definicionMatriz
                            | expresionPostfijo
                            '''
        if len(p) == 3:
            p[0] = ('expresionAsignacion', p[1], p[2])  
        else:  
            p[0] = ('expresionAsignacion', p[1])

    #<expresionConstante> ::= constant <expresionAsignacion>
    def p_expresionConstante(self,p):
        '''expresionConstante : CONSTANT expresionAsignacion'''
        p[0] = ('expresionConstante', p[2])

    #<operadorAsignacionAritmetico> ::= += | -= | *= | /=
    def p_operadorAsignacion(self,p):
        '''operadorAsignacion : IGUAL
                            | MAS_IGUAL
                            | MENOS_IGUAL
                            | POR_IGUAL
                            | DIVISION_IGUAL'''
        p[0] = p[1]   
    #----------------------------------------------------------------------------------------------------------

    #---------------------------- L L A M A D A   A   M E T O D O S -------------------------------------------
    #<llamadaMetodo> ::= <metodoAxol> | this . IDENTIFICADOR 
    def p_llamadaMetodo(self,p):
        '''llamadaMetodo : THIS PUNTO IDENTIFICADOR PARENTESIS_ABRE argumentos 
                        | metodoAxol PARENTESIS_ABRE argumentos '''
        if len(p) == 6:
            p[0] = ('llamadaMetodo', p[1]) 
        else:
            p[0] = ('llamadaMetodo', p[1], p[2]) 

    #<metodoAxol> ::= (read_key | read_bin | read_tec | save_bin | print |print_con | pop | push | position |
    #               show | positionX | positionY | add | set | random | getPosition | size | rotate)
    def p_metodoAxol(self,p):
        '''metodoAxol : READ_BIN
                    | READ_TEC
                    | SAVE_BIN
                    | PRINT
                    | PRINT_CON
                    | SHOW
                    | POSITIONX
                    | POSITIONY
                    | RANDOM
                    | GETPOSITION'''
        p[0] = ('metodoAxol', p[1])

    # <argumentos> ::= (expresion | objeto) <restoArgumentos> PARENTESIS_CIERRA
    def p_argumentos(self,p):
        '''argumentos : expresion restoArgumentos PARENTESIS_CIERRA
                    | objeto restoArgumentos PARENTESIS_CIERRA
                    | valorCadena restoArgumentos PARENTESIS_CIERRA
                    | booleano restoArgumentos PARENTESIS_CIERRA
                    | direction restoArgumentos PARENTESIS_CIERRA
                    | PARENTESIS_CIERRA'''
        if len(p) == 4:  # Caso con expresión u objeto, restoArgumentos y paréntesis de cierre
            p[0] = ('argumentos', p[1], p[2])
        else:  # Caso sin argumentos, solo paréntesis de cierre
            p[0] = ('argumentos',)

    #<restoArgumentos> ::= , <argumentos> | ε
    def p_restoArgumentos(self,p):
        '''restoArgumentos : COMA expresion restoArgumentos
                        | COMA objeto restoArgumentos
                        | COMA valorCadena restoArgumentos
                        | COMA booleano restoArgumentos
                        | COMA direction restoArgumentos
                        | empty'''
        if len(p) == 3:
            p[0] = ('restoArgumentos', p[2])  # Caso con argumentos adicionales
        else:
            p[0] = ('restoArgumentos',)  # Caso ε (sin más argumentos)
    #----------------------------------------------------------------------------------------------------------

    #-------------------------------------------- V A L O R E S -----------------------------------------------
    #<booleano> ::= true | false
    def p_booleano(self,p):
        '''booleano : TRUE
                    | FALSE'''
        p[0] = ('booleano', p[1])

    #<direction> ::= up | down | left | right
    def p_direction(self,p):
        '''direction : UP
                    | DOWN
                    | LEFT
                    | RIGHT'''
        p[0] = ('direction', p[1])

    #<valorCadena>
    def p_valorCadena(self,p):
        '''valorCadena : VALOR_CHAR
                    | VALOR_STRING'''
        p[0] = p[1]

    #<objeto> ::= new <clase>(<argumentos>)
    def p_objeto(self,p):
        '''objeto : NEW IDENTIFICADOR PARENTESIS_ABRE argumentos'''
        p[0] = ('objeto', p[2], p[4])
    #----------------------------------------------------------------------------------------------------------

    #------------------------------- E S T R U C T U R A   D E   D A T O S ------------------------------------
    # <estructuraDatos> ::= <arreglo> | <matriz>
    def p_declaracionEstructuraDatos(self,p):
        '''declaracionEstructuraDatos : declaracionArreglo
                                    | declaracionMatriz'''
        p[0] = ('declaracionEstructuraDatos', p[1])

    # <declaracionArreglo> ::= 
    def p_declaracionArreglo(self,p):
        '''declaracionArreglo : declaracionArregloSimple PUNTO_Y_COMA
                            | declaracionArregloSimple IGUAL fila PUNTO_Y_COMA'''
        if len(p) == 3:
            # Caso de declaración de arreglo simple, sin asignación
            p[0] = ('declaracionArreglo', p[1])
        else:
            # Caso de declaración de arreglo con asignación de una fila (elementos del arreglo)
            p[0] = ('declaracionArreglo', p[1], p[3])

    # <declaracionArreglo> ::=  
    def p_declaracionMatriz(self,p):
        '''declaracionMatriz  : declaracionMatrizSimple PUNTO_Y_COMA
                            | declaracionMatrizSimple IGUAL CORCHETE_ABRE filas CORCHETE_CIERRA PUNTO_Y_COMA'''
        if len(p) == 3:
            # Caso de declaración de matriz sin inicialización
            p[0] = ('declaracionMatriz', p[1])
        else:
            # Caso de declaración de matriz con asignación de filas (contenidos entre corchetes)
            p[0] = ('declaracionMatriz', p[1], p[4])

    # <declaracionArregloSimple> ::= <tipoDato> [ numero ] identificador ;
    def p_declaracionArregloSimple(self,p):
        '''declaracionArregloSimple : tipoDato IDENTIFICADOR CORCHETE_ABRE NUMERO CORCHETE_CIERRA'''
        p[0] = ('declaracionArregloSimple', p[1])

    # <declaracionMatrizSimple> ::= <tipoDato> [ numero ] [ numero ] identificador ;
    def p_declaracionMatrizSimple(self,p):
        '''declaracionMatrizSimple : tipoDato IDENTIFICADOR CORCHETE_ABRE NUMERO CORCHETE_CIERRA CORCHETE_ABRE NUMERO CORCHETE_CIERRA'''
        p[0] = ('declaracionMatrizSimple', p[1])

    # <filas> ::= <fila> <restoFilas>
    def p_filas(self,p):
        '''filas : fila restoFilas'''
        p[0] = ('filas', p[1], p[2])

    # <restoFilas> ::= , <filas> | ε
    def p_restoFilas(self,p):
        '''restoFilas : COMA filas
                    | empty'''
        if len(p) == 3:
            p[0] = ('restoFilas', p[2])
        else:
            p[0] = ('restoFilas', [])

    # <fila> ::= [ <elementosFila> ]
    def p_fila(self,p):
        '''fila : CORCHETE_ABRE elementosFila CORCHETE_CIERRA'''
        p[0] = ('fila', p[2])

    # <elementosFila> ::= <expresion> <restoElementosFila>
    def p_elementosFila(self,p):
        '''elementosFila : expresion restoElementosFila
                        | valorCadena restoElementosFila
                        | booleano restoElementosFila'''
        p[0] = [p[1]] + p[2]

    # <restoElementosFila> ::= , <elementosFila> | ε
    def p_restoElementosFila(self,p):
        '''restoElementosFila : COMA elementosFila
                            | empty'''
        if len(p) == 2:  # Caso de ε
            p[0] = []
        else:  # Caso con coma
            p[0] = p[2]

    # <definicionArreglo> ::= <identificador> = [ <elementosArreglo> ] 
    def p_definicionArreglo(self,p):
        '''definicionArreglo : IDENTIFICADOR IGUAL fila'''
        p[0] = ('definicionArreglo', p[3])

    def p_definicionMatriz(self,p):
        '''definicionMatriz : IDENTIFICADOR IGUAL CORCHETE_ABRE filas CORCHETE_CIERRA'''
        p[0] = ('definicionMatriz', p[4])

    # <accesoLineal> ::= <identificador> [ numero ]
    def p_accesoLineal(self,p):
        '''accesoLineal : IDENTIFICADOR CORCHETE_ABRE NUMERO CORCHETE_CIERRA'''
        p[0] = ('accesoLineal', p[1], p[3])  # Tupla con el identificador y el índice

    # <accesoMatriz> ::= <identificador> [ numero  ] [ numero ]
    def p_accesoMatriz(self,p):
        '''accesoMatriz : IDENTIFICADOR CORCHETE_ABRE NUMERO CORCHETE_CIERRA CORCHETE_ABRE NUMERO CORCHETE_CIERRA'''
        p[0] = ('accesoMatriz', p[1], p[2])
    #----------------------------------------------------------------------------------------------------------

    #---------------------------------------------- V A C I O -------------------------------------------------
    # Producción para vacío (ε)
    def p_empty(self,p):
        'empty :'
        pass
    #----------------------------------------------------------------------------------------------------------

    #---------------------------------------------- E R R O R -------------------------------------------------
    def p_error(self,p):
        if p:
            mensaje_error=(f"Error de sintaxis en '{p.value}', en la linea '{p.lineno}'")
            print(mensaje_error)
            self.errores.append([mensaje_error,p.lineno,p.lexpos])
            print(self.errores)
        else:
            print("Error de sintaxis al final de la entrada")
    #----------------------------------------------------------------------------------------------------------