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
           boolean resultado = -3;

            method boolean miMetodo () {
                print(nombre);
                return flag;
            }

           axol2D play () {
                this.miMetodo();
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
