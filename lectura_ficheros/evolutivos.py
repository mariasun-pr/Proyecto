from lectura_ficheros.rules_file import *
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

        for i in range(len(lineas)):
            linea = lineas[i]
            linea = linea.rstrip()
            if(linea.__contains__('Antecedent')):
                nombreRegla = "Regla " + str(numRegla) + " IF "
                numRegla += 1

                valorAtributos = [None] * numAtributos
                operadores = [None] * numAtributos

            elif(linea.__contains__('Variable')):
                linea = linea.split(' ')
                if(not lineas[i+1].__contains__('Consecuent')):
                    nombreRegla += linea[1] + " "+ linea[2] + " " +linea[3] + " AND "
                else:
                    nombreRegla += linea[1] + " "+ linea[2] + " " +linea[3]

                try:
                    index = dataset.atributos.index(linea[1])
                except:
                    print('Error')

                valorAtributos[index] = linea[3]
                operadores[index] = linea[2]

            elif(linea.__contains__('Consecuent')):
                linea = linea.replace('   ', '')
                linea = linea.split(' ')
                clase = linea[1]
                nombreRegla += " THEN class = " + linea[1]

                regla = Regla(valorAtributos, clase, nombreRegla, operadores)
                self.reglas.append(regla)

        return self.reglas
