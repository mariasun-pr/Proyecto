from lectura_ficheros.rules_file import *
from lectura_ficheros.dataset import *
from utils.regla import *
import re

class Apriori(lecturaFicheroReglas):
    def lecturaFichero(self, fichero, dataset):
        self.fichero = open(fichero)
        lineas = self.fichero.readlines()

        self.reglas = []

        for i in range (len(lineas)):
            linea = lineas[i]
            linea = linea.rstrip()

            if(linea.__contains__("IF")):
                nombreRegla = re.sub(r'--.*', "", linea) 
                
                linea = linea.split(' ')

                numAtributos = len(dataset.atributos)
                valorAtributos = [None] * numAtributos
                operadores = [None] * numAtributos

                for j in range (numAtributos):
                    index = -1
                    try:
                        index = linea.index(dataset.atributos[j])
                    except:
                        index = -1
                    if(index >= 0):
                        valorAtributos[j] = linea[index + 3]
                        operadores[j] = linea[index + 1]

                try:
                    index = linea.index('Class')
                except:
                    try:
                        index = linea.index('class')
                    except:
                        "Error"
                clase = linea[index + 2]

                regla = Regla(valorAtributos, clase, nombreRegla, operadores)
                self.reglas.append(regla)

        return self.reglas

