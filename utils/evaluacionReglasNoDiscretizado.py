import numpy as np


class evaluacionReglasNoDiscretizado:
    def evaluarReglas(self, dataset, reglas):
        self.reglas = reglas
        self.dataset = dataset
        intervalos = []
        self.numEtiquetas = reglas[0].numEtiquetas
        self.dividirIntervalos(intervalos)

        for regla in reglas:
            truePositive = 0
            trueNegative = 0
            falsePositive = 0
            falseNegative = 0

            for dato in dataset.datos:
                contOcurrencias = 0
                contValoresAtributosRegla = 0

                for i in range(len(regla.atributos)):
                    if (regla.atributos[i] != None):
                        contValoresAtributosRegla += 1
                        etiqueta = self.funcionPertenencia(intervalos[i], dato[i])
                        if (regla.atributos[i] == str(etiqueta)):
                            contOcurrencias += 1

                if (dato[len(regla.atributos)] == regla.clase):
                    if (contOcurrencias == contValoresAtributosRegla):
                        truePositive += 1
                        dataset.anadirRegla(dato, regla)
                        regla.datosCubre.append(dato)
                    else:
                        falseNegative += 1

                if (dato[len(regla.atributos)] != regla.clase):
                    if (contOcurrencias == contValoresAtributosRegla):
                        falsePositive += 1
                    else:
                        trueNegative += 1

            regla.tp = truePositive
            regla.tn = trueNegative
            regla.fp = falsePositive
            regla.fn = falseNegative

            regla.tpr = round(
                (truePositive / (truePositive + falseNegative))*100, 2)
            regla.fpr = round(
                (falsePositive / (falsePositive + trueNegative))*100, 2)
            
        for regla in reglas:
            regla.mostrar()

    def dividirIntervalos(self, intervalos):
        for interval in self.dataset.intervalos:
            interval = interval.replace('[', '').replace(']', '').split(',')
            inicio = float(interval[0])
            fin = float(interval[1])
            intervalo = np.linspace(inicio, fin, self.numEtiquetas)
            diferencia = intervalo[1] - intervalo[0]
            primerValor = intervalo[0] - diferencia
            ultimoValor = intervalo[self.numEtiquetas-1]+diferencia

            intervalo = list(intervalo)
            intervalo.insert(0, round(primerValor, 2))
            intervalo.append(round(ultimoValor, 2))
            intervalos.append(intervalo)

    def funcionPertenencia(self, intervalo, valor):
        etiqueta = -1
        pertenencia = -1.0
        y = 1.0
        calculo = -1.0
        valor = float(valor)
        y = float(y)
        for i in range (self.numEtiquetas):
            x0 = float(intervalo[i])
            x1 = float(intervalo[i+1])
            x2 = float(intervalo[i+2])

            if (valor<x1):
                calculo = ((valor-x0)*(y/(x1-x0)))
            if (valor>x1):
                calculo = ((x2-valor)*(y/(x2-x1)))
            
            if(calculo > pertenencia):
                pertenencia = calculo
                etiqueta = i
                calculo = -1

        return etiqueta






