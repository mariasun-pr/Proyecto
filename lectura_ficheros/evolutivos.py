from lectura_ficheros.lecturaFicheroReglas import *
from lectura_ficheros.dataset import *
from utils.regla import *
import re


class Evolutivos(lecturaFicheroReglas):
    def lecturaFichero(self, fichero, dataset):
        self.fichero = open(fichero)
        lineas = self.fichero.readlines()

        self.reglas = []
        numAtributos = len(dataset.atributos)
        numRegla = 1
        numEtiquetas = -1

        for i in range(len(lineas)):
            linea = lineas[i]
            linea = linea.rstrip()
            if(linea.__contains__('Antecedent')):
                nombreRegla = "Rule " + str(numRegla) + ": IF "
                numRegla += 1

                valorAtributos = [None] * numAtributos
                operadores = [None] * numAtributos

            elif(linea.__contains__('Variable')):
                linea = linea.split(' ')
                if(linea.__contains__('Label')):
                    valor = 4
                else:
                    valor = 3
                if(not lineas[i+1].__contains__('Consecuent')):
                    nombreRegla += linea[1] + " "+ linea[2] + " " +linea[valor] + " AND "
                else:
                    nombreRegla += linea[1] + " "+ linea[2] + " " +linea[valor]

                try:
                    index = dataset.atributos.index(linea[1])
                except:
                    print('Error')

                valorAtributos[index] = linea[valor]
                operadores[index] = linea[2]

            elif(linea.__contains__('Number of labels')):
                linea = linea.replace('Number of labels: ', '')
                numEtiquetas = int(linea)

            elif(linea.__contains__('Consecuent')):
                linea = linea.replace('   ', '')
                linea = linea.split(' ')
                clase = linea[1]
                nombreRegla += " THEN class = " + linea[1]

                regla = Regla(valorAtributos, clase, nombreRegla, operadores, numEtiquetas)
                self.reglas.append(regla)

        return self.reglas
