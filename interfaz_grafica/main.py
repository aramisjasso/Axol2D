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
        # '''
        # import Background;
        # import Players;

        # level MiPrimerNivel {
        #     int x = 0;
        #                 // [Tam_x, Tam_y, posi_x, posi_y,  R   ,  G   ,  B  ]
        #     platform pl = [140  ,   10 ,   10  , 10     , 150 , 150  ,  150 ];
        #     platform pl = [110  ,   20 ,   20  , 10     ,  0  ,  0   ,   0  ];
        #     platform plarreglo[5];
        #     platform elementos_fondo[0];

        #     obstacles obs [0];
        #     background fondo = Background.castel;
        #                    //[inicio x, inicio y, vidas, personaje       ]
        #     player jugador = [   0    ,    0    ,   3  , Players.mario   ];
        #     method int llenadoObs(){
        #         x=0
        #         while (x<5){
        #         obs[x]=[140  ,   10 ,   x*10  , 10     , 150 , 150  ,  150 ]
        #         }


        #         return 0;
        #     }
            
        #    axol2D play () {
        #         this.llenadoObs()
        #                         // (Fila_pla, fila_obs ,Jugador, Fondo ,  elementos_fondo, Posión a llegar)
        #         MiPrimerNivel.start(pl      ,   obs    ,jugador, fondo ,  elementos_fondo,  [100,100]     );
        #    }
        # }'''
                '''
        import Background;
        import Players;


        level MiPrimerNivel {
            int x = 0;
            int y = 1;
            int a1 = 0;
            int a3 = 15;
            string b = "cadena";
            byte a2 = 0;
            int matriz [3][4] = [[1,2,3,4],[4,5,6,7],[7,8,9,0]];
                        // [posi_x, posi_y, tam_x, tam_y,  R   ,  G   ,  B  ]
            platform pl1 = [0  ,   24 ,   5  , 1        ,  48  ];
            platform pl2 = [5  ,   23 ,   5  , 1        ,  48  ];
            platform pl3 = [10  ,   22 ,   5  , 1       ,  48  ];
            platform pl4 = [15  ,   21 ,   5  , 1       ,  48  ];
            platform pl5 = [20  ,   20 ,   5  , 1       ,  48  ];
            platform pl6 = [25  ,   19 ,   5  , 1       ,  48  ];

            platform plarreglo[6] = [pl1, pl2, pl3, pl4, pl5, pl6];
            obstacles obs1 = [0  ,   0 ,   5  , 1     , 64 ];
            obstacles obs2 = [5  ,   1 ,   5  , 1     ,  64  ];
            obstacles obs [2] = [obs1,obs2];
            
            background fondo = Castle;
            int fin [2] = [100,100];
                           //[inicio x, inicio y, vidas, personaje       ]
            player jugador = [   0    ,    0    ,   3  , knight   ];
            method int miMetodo1(){
                a1 = 12;
                pl1 = [200  ,   200 ,   200  , 200     , 200 ];
                while (x<5){
                    //obs[{x}] = [110  ,   20 ,   20  , 10     ,  0 ];
                    obs[0] = [110  ,   20 ,   20  , 10     ,  0];
                }
                
                return 0;
            }

            method int miMetodo2(){
                a1 = 12;

                return 0;
            }  
            method int miMetodo3(int a , int c){
                a1 = 12;
                this.miMetodo3(a,12);
                return 0;
            }          
            
           axol2D play () {
                b = "b";
                matriz[0][2] = 1;
                //a1 = this.miMetodo3(123,2);
                // (Fila_pla, fila_obs ,Jugador, Fondo ,  elementos_fondo, Posión a llegar)
                MiPrimerNivel.start(plarreglo , obs , jugador , fondo ,  plarreglo,     fin  );
           }
        }'''
        # '''
        # level MiPrimerNivel {
        #     int numeros [5][1];  
        #     int a1;

        #     method int sumar (int a, int b) {
        #         numeros [0][0] = 0;
        #         pl1 = [200, 200, 200, 200, 200, 200, 200];
        #         this.sumar("Hola",b);
        #         a1 = this.sumar("Hola",b);
        #         return 0;
        #     }

        #     axol2D play () {
        #         0;
        #     }
        # }
        # '''
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