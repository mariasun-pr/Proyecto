import re
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
                if("real" in lineas[i] and self.algoritmo in ALGORITMOS_NO_CONTINUOS):
                    print("Tiene que ser el dataset discretizado")
                    return "No discretizado"
                else:
                    compruebaDiscreto = True

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
        self.reglasCubren = [None] * len(self.datos)
        #!Probablemente borrar línea de abajo y función
        # self.tratarDataset()

        # Si la carga se ha producido correctamente
        return "True"

    def tratarDataset(self):
        self.valoresAtributoPorClase = []

        for clase in self.clases:
            valorAtributos = [None] * len(self.atributos)
            for dato in self.datos:
                if(clase in dato):
                    for i in range(len(self.atributos)):
                        if(valorAtributos[i] == None):
                            valorAtributos[i] = dato[i]
                        elif (dato[i] not in valorAtributos[i]):
                            valorAtributos[i] = valorAtributos[i] + \
                                ' ' + dato[i]

            self.valoresAtributoPorClase.append(valorAtributos)

            print(valorAtributos)

    def anadirRegla(self, dato, regla):
        nombreRegla = re.sub(r':.*', "", regla.nombre)
        valor = self.reglasCubren[self.datos.index(dato)]
        if(valor != None and nombreRegla not in valor):
            self.reglasCubren[self.datos.index(dato)] += ", " + nombreRegla
        elif(valor == None):
            self.reglasCubren[self.datos.index(dato)] = nombreRegla
