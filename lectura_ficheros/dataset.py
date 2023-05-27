import re
from utils.constantes import *


class lecturaDataset:
    def __init__(self, nombreFichero, algoritmo):
        self.nombreFichero = nombreFichero
        self.algoritmo = algoritmo
        self.intervalos = []

    def lecturaFichero(self, discretizado):
        fichero = open(self.nombreFichero)
        lineas = fichero.readlines()

        self.atributos = []
        self.clases = []
        self.datos = []
        compruebaDiscreto = False
        almacenarDatos = False

        if(not "@data\n" in lineas):
            return "Formato incorrecto"

        for i in range(len(lineas)):
            linea = lineas[i]
            linea = linea.rstrip()

            # Obtener clases del dataset
            if("@attribute" in lineas[i] and "@inputs" in lineas[i+1]):
                linea = re.sub(r'}.*', "", linea)
                linea = re.sub(r'^.*?(?=\{)', "", linea)
                linea = linea.replace('{', '').replace(', ', ',')
                self.clases = linea.split(',')
                print(self.clases)

            # Comprobar tipo de atributo del dataset
            elif("@attribute" in lineas[i] and not compruebaDiscreto):
                if(("real" in lineas[i] or "integer" in lineas[i]) and ((self.algoritmo not in ALGORITMOS_EVOLUTIVOS) or (discretizado and self.algoritmo in ALGORITMOS_EVOLUTIVOS))):
                    print("Tiene que ser el dataset discretizado")
                    return "No discretizado"
                elif((not "real" in lineas[i] and not "integer" in lineas[i]) and not discretizado):
                    print("El dataset no tiene que estar discretizado")
                    return "Discretizado"
                else:
                    compruebaDiscreto = True

            #Obtener intervalo real 
            if("@attribute" in linea and "real" in linea):
                linea = lineas[i].split(" ")
                intervalo = linea[len(linea)-2] + linea[len(linea)-1]
                print(intervalo)
                self.intervalos.append(intervalo)

            # Obtener atributos del dataset
            elif("@inputs" in lineas[i]):
                linea = linea.replace('@inputs ', '')
                linea = linea.replace(', ', ',')
                self.atributos = linea.split(',')

                print(self.atributos)

            # Para indicar que a partir de aquí solo se almacenan datos
            elif("@data" in lineas[i]):
                almacenarDatos = True

            # Almacenamiento de los datos
            elif(almacenarDatos and linea != ''):
                linea = linea.replace(', ', ',')
                linea = linea.split(',')
                self.datos.append(linea)

        # Inicializo el atributo que almacen las reglas que cubren al dato
        self.reglasCubrenBien = [None] * len(self.datos)
        self.reglasCubrenMal = [None] * len(self.datos)

        # Si la carga se ha producido correctamente
        return "True"

    def anadirRegla(self, dato, regla, cubiertoBien, disparo = -2):
        nombreRegla = re.sub(r':.*', "", regla.nombre)
        if(disparo != -2):
            nombreRegla += "("+str(disparo)+")"
        if(cubiertoBien):
            valor = self.reglasCubrenBien[self.datos.index(dato)]
            if(valor != None and nombreRegla not in valor):
                self.reglasCubrenBien[self.datos.index(dato)] += ", " + nombreRegla
            elif(valor == None):
                self.reglasCubrenBien[self.datos.index(dato)] = nombreRegla
        else:
            valor = self.reglasCubrenMal[self.datos.index(dato)]
            if(valor != None and nombreRegla not in valor):
                self.reglasCubrenMal[self.datos.index(dato)] += ", " + nombreRegla
            elif(valor == None):
                self.reglasCubrenMal[self.datos.index(dato)] = nombreRegla
