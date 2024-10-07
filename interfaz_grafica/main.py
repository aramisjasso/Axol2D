import compilador.compilador as compilador


# Prueba de ambos
if __name__ == "__main__":
    # Define algunas pruebas
    pruebas = [
        # 'int a = 5;',
        # '(x+3*(y-8)/z)-(a+6)*b'
        # '''for(int i = 0; i < 10; i++) {
        #         a[0] += i;
        #         print(i);
        #    }''',
        # '''while(a < 10) {
        #     bandera = this.metodoBooleano(x, z);
        #     arrar[3] *= 3;
        # }''',

        # '''switch (a) {
        #     case 1: 
        #         cadenas = ["cadena1", "cadena2", "cadena3"]; 
        #         break;
        #     case 2: 
        #         array[1] = 3*5;
        #         break;
        #     default: 
        #         numeros = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
        # }''', 
        # 'int a[3] = [cadena1,cadena, cadena2]; ', 
        # 'int a [5] ;'
        '''
        import Controllers;
        import enemies;

        level MiPrimerNivel {
            boolean resultado = true;
            boolean resultado2 = resultado;
            
            method int miMetodo1(string b, int a1, int c){
                a1 = 12;
                return 0;
            }
            
           axol2D play () {
                MiPrimerNivel.start();
           }
        }'''
    ]
    
    for prueba in pruebas:
        print(f"\nProbando: {prueba}\n")
        compilador = compilador.Compilador()
        compilador.compilar(prueba)
        x=compilador.errores_re()
        print(x)

# ------------- Testeo ---------------------
# Truena con: 
# boolean a;
# byte c = a;
# 
# byte c = True;

# '''
#         import Controllers;
#         import enemies;

#         level MiPrimerNivel {
#             string nombre = "cadena";
#             /°int numeros [5] = [0, 1, 2, 3, 4];
#             byte a123 = 1;
#             int identificador = 0; °/
#             boolean resultado = true;
#             boolean resultado2 = resultado;
#             //string nombre2 = nombre;
            
#             /°int arreglo [6] = [1,2,3,4,5,6];
#             int a = 1;
#             int arreglo1 [6] = [arreglo[5],a,a,a,a,a];
#             int arreglo2 [2][3] = [[1,2,3],[4,5,6]];
#             int b1 = arreglo2[1][1];
#             char letra = 'a';°/
            
#             method int miMetodo1(string b,int a1,int c){
#                 a1 = 12;
#                 //arreglo = [1,1,a,a,a,a];
#                 //arreglo2 = [['a',b,a],[a,a,a]];
#                 //b2 = a1;
#                 //arreglo1[0]=1;
#                 return 0;
#             }
            
#             method string miMetodo2(string b,int a1, int c) {
#                 a1 = 12;
#                 /°
#                 arreglo[1]=1;
#                 arreglo = [1,1,a,a,a,a];
#                 //arreglo2 = [['a',b,a],[a,a,a]];
#                 //reglo[1] = a;
#                 //sds=a;
#                 a=1;
#                 //b2 = a1;
#                 arreglo1[0]=1;
#                 //resultado = resultado;
#                 //nombre2 = nombre;
#                 //miMetodo2 = 1;
#                 //this.miMetodo1 (nombre,a,c);°/
#                 return nombre;
#             }


#            axol2D play () {
#                 //a = 10;
#                 MiPrimerNivel.start();
#            }
#         }'''