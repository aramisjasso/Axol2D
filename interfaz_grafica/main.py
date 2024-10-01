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
            int a = 0;
            int b =3;
            byte c = 16;
            string d = "mi Cadenon";
            char x;
            int x1 [5] = [1,2,3,4,5];
            int x2 [5];
            int y1 [5][1];
            int x3 [3][2]=[[1,2],[3,4],[5,6]];

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
        compilador = compilador.Compilador()
        compilador.compilar(prueba)
        x=compilador.errores_re()
        print(x)