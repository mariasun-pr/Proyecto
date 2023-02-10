
from constantes.utils import *

class lecturaDataset:
    def __init__(self, nombreFichero, algoritmo):
        self.nombreFichero = nombreFichero
        self.algoritmo = algoritmo

    def lecturaFichero(self):
        fichero = open(self.nombreFichero)
        lineas = fichero.readlines()

        self.atributos = []
        self.clases = []
        self.datos = []
        compruebaDiscreto = False
        almacenarDatos = False

        for i in range (len(lineas)):
            #print (lineas[i])
            linea = lineas[i]
            linea = linea.rstrip()

            #Obtener clases del dataset
            if("@attribute" in lineas[i] and "@inputs" in lineas[i+1]):   
                linea = linea.replace('class', '').replace('@attribute', '').replace('}', '').replace('{', '').replace(' ','')
                clases = linea.split(',')#{x.replace('class', '').replace('@attribute', '').replace('}', '').replace('{', '') for x in lineas[i]}
                self.clases = clases
                print(self.clases)

            #Comprobar tipo de atributo del dataset
            elif("@attribute" in lineas[i] and not compruebaDiscreto):
                if("real" in lineas[i] and self.algoritmo in ALGORITMOS_NO_CONTINUOS):
                    print("Tiene que ser el dataset discretizado")
                    return False
                else:
                    compruebaDiscreto = True
            
            #Obtener atributos del dataset
            elif("@inputs" in lineas[i]):
                linea = linea.replace('@inputs ', '')
                self.atributos = linea.split(',')

                print(self.atributos)

            elif("@data" in lineas[i]):
                almacenarDatos = True

            elif(almacenarDatos):
                self.datos.append(linea)

                #print(self.datos)


        return True
                
        




