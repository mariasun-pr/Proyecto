from lectura_ficheros.rules_file import *
from lectura_ficheros.dataset import *
from utils.regla import *
import re


class SdMap(lecturaFicheroReglas):
    def lecturaFichero(self, fichero, dataset):
        self.fichero = open(fichero)
        lineas = self.fichero.readlines()

        self.reglas = []
        clase = ''
        numAtributos = len(dataset.atributos)

        for i in range(len(lineas)):
            linea = lineas[i]
            linea = linea.rstrip()

            #if(linea.__contains__('Target Variable')):
            #    linea = linea.split(' ')
            #    try:
            #        index = linea.index('=')
            #    except:
            #        print("Error")

            #   clase = linea[index + 1]


            if(linea.__contains__("THEN")):
                nombreRegla = linea

                linea = linea.split(' ')

                valorAtributos = [None] * numAtributos
                operadores = [None] * numAtributos

                for j in range(numAtributos):
                    index = -1

                    # Comprueba si la regla da valor al atributo j, si sí almacena el valor y el operador utilizado
                    try:
                        index = linea.index(dataset.atributos[j])
                    except:
                        index = -1
                    if(index >= 0):
                        valorAtributos[j] = linea[index + 2]
                        operadores[j] = linea[index + 1]

                try:
                    index = linea.index('THEN')
                except:
                    print("Error")

                clase = linea[index + 3]

                regla = Regla(valorAtributos, clase, nombreRegla, operadores, -1)
                self.reglas.append(regla)

        return self.reglas