import os
from pathlib import Path
class ejecutar():
    def __init__(self):
        self.ASM = """"""
        self.nombre_archivo = ""
    
    #Run
    def run(self,contenido,archivo):
        self.nombre_archivo  = f"{Path(archivo).name}".split(".")[0] #Deja solo el nombre del archivo
        self.ASM=contenido
        print("Inicio .exe")
        self.fnCrearASM()
        self.fnCrearObj()
        self.fnCrearExe()
        print ("Fin .exe")
    
    #Crear ASM
    def fnCrearASM(self):
        #Creación ASM
        with open(f"{self.nombre_archivo}.asm", 'w') as file:
            file.write(self.ASM)

        print(f"Archivo '{ self.nombre_archivo}' creado con éxito.")

    def fnCrearObj(self):
        #Construcción del comando para ejecutar
        comando = f"masm /coff \"{self.nombre_archivo}.asm\""

        # Ejecutar el comando
        os.system(comando)
        print(f"Archivo generado correctamente: {self.nombre_archivo}.obj")

    def fnCrearExe(self):
        #Construcción del comando para ejecutar
        comando = f"golink /console \"{self.nombre_archivo}.obj\" kernel32.dll user32.dll"

        # Ejecutar el comando
        os.system(comando)
        print(f"Archivo generado correctamente: {self.nombre_archivo}.exe")

        comando = f"\"{self.nombre_archivo}.exe\""

        # Ejecutar el comando
        os.startfile(comando)
        print(f"Archivo Ejecutado correctamente: {self.nombre_archivo}.exe")
    #Crear carpeta si no existe
    def fnCrearCarpeta (self, carpeta):
        if not carpeta.exists():
            carpeta.mkdir(parents=True, exist_ok=True)  # 'parents=True' crea las carpetas intermedias si es necesario
            print(f"Carpeta '{carpeta}' creada con éxito.")
        else:
            print(f"La carpeta '{carpeta}' ya existe.")