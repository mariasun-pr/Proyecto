
from utils.constantes import *

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
            linea = lineas[i]
            linea = linea.rstrip()

            #Obtener clases del dataset
            if("@attribute" in lineas[i] and "@inputs" in lineas[i+1]):   
                linea = linea.replace('class', '').replace('@attribute', '').replace('}', '').replace('{', '').replace(' ','').replace('Class', '')
                clases = linea.split(',')
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
                linea = linea.replace(', ', ',')
                self.atributos = linea.split(',')

                print(self.atributos)

            elif("@data" in lineas[i]):
                almacenarDatos = True

            elif(almacenarDatos):
                linea = linea.replace(', ', ',')
                linea = linea.split(',')
                self.datos.append(linea)

                #print(self.datos)
        self.tratarDataset()
        #Si la carga se ha producido correctamente
        return True
    

    def tratarDataset(self):
        self.valoresAtributoPorClase = []

        for clase in self.clases:
            valorAtributos = [None] * len(self.atributos)
            for dato in self.datos:
                if(clase in dato):
                    for i in range (len(self.atributos)):
                        if(valorAtributos[i] == None):
                            valorAtributos[i] = dato[i]
                        elif (dato[i] not in valorAtributos[i]):
                            valorAtributos[i] = valorAtributos[i] + ' ' + dato[i]
            
            self.valoresAtributoPorClase.append(valorAtributos)

            print(valorAtributos)







    

        




