import compilador.lexico as lexico
import compilador.sintactico as sintactico

# Función de prueba para el parser
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
        self.compilo = True #Si compilo
        self.varId = 0

    def compilar(self,data):
        self.parte_Lexico(data)
        self.parte_Sintactica(data,self.lexi.lexer)

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
            print(tok)
        self.errores_lexicos = self.lexi.errores
        self.lexi.errores=[]
        if self.errores_lexicos == []:
            self.compilo=True
        else:
            self.compilo=False

    def parte_Sintactica(self,data,lexer):
        self.sin.build()
        lexer.lineno = 1 #Reincia el número de linea
        try:
            resultado = self.sin.parser.parse(data, lexer=lexer ,tracking=True)
            if resultado:
                print("Análisis sintáctico exitoso:", resultado)
                #print("Análisis sintáctico completado pero sin resultado (posiblemente vacío)")
            if self.sin.errores !=[]:
                self.compilo = False
                self.errores_sintacticos=self.sin.errores
        except Exception as e:
            print(f"Error durante el análisis sintáctico: {e}")
    #Errores
    def errores_re(self):
        mensajes=''
        self.errores_lista = self.errores_lexicos+self.errores_sintacticos
        self.errores_lista= sorted(self.errores_lista, key=lambda x:x[2])
        for error in self.errores_lista:
            mensajes+=(f"{error[0]}" +'\n')
        return mensajes

# Prueba de ambos
if __name__ == "__main__":
    # Define algunas pruebas
    pruebas = [
        'int a = 5;',
        '(x+3*(y-8)/z)-(a+6)*b'
        '''for(int i = 0; i < 10; i++) {
                a[0] += i;
                print(i);
           }''',
        '''while(a < 10) {
            bandera = this.metodoBooleano(x, z);
            arrar[3] *= 3;
        }''',

        '''switch (a) {
            case 1: 
                cadenas = ["cadena1", "cadena2", "cadena3"]; 
                break;
            case 2: 
                array[1] = 3*5;
                break;
            default: 
                numeros = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
        }''', 
        'cadenas = ["cadena1", "cadena2", "cadena3"]; ', 
        '''
        import Controllers;
        import enemies;

        level MiPrimerNivel {
            int a = 0;
            int b = 2;
            byte c = 16;
            string d = "mi Cadenon";
            char x;

            method boolean miMetodo (int a, int b, byte c, string d, char x) {
                if (a==b) { 
                    x = a + b - c * d;
                    print(x);
            }
            return x;
           }

           axol2D play () {
                this.miMetodo(2, 3, 4, "aramis", 'x');
                z += 3;
                MiPrimerNivel.start();
           }
        
        }'''
    ]
    
    for prueba in pruebas:
        print(f"\nProbando: {prueba}")
        compilador = Compilador()
        compilador.compilar(prueba)
        print(compilador.errores_re)
