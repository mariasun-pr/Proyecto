import numpy as np


class evaluacionReglasNoDiscretizado:
    def evaluarReglas(self, dataset, reglas):
        self.reglas = reglas
        self.dataset = dataset
        intervalos = []
        self.numEtiquetas = reglas[0].numEtiquetas
        self.dividirIntervalos(intervalos)
        numDatos = len(dataset.datos)

        for regla in reglas:
            truePositive = 0
            trueNegative = 0
            falsePositive = 0
            falseNegative = 0
            contDato = 0
            for dato in dataset.datos:
                contDato += 1
                contOcurrencias = 0
                contValoresAtributosRegla = 0
                calculoFinal = 1000
                for i in range(len(regla.atributos)):
                    if (regla.atributos[i] != None):
                        contValoresAtributosRegla += 1
                        etiqueta, calculo = self.funcionPertenencia(intervalos[i], dato[i])
                        if (regla.atributos[i] == str(etiqueta)and calculo >= 0.5):
                            contOcurrencias += 1
                            if(calculo < calculoFinal):
                                calculoFinal = calculo

                if (dato[len(regla.atributos)] == regla.clase):
                    if (contOcurrencias == contValoresAtributosRegla):
                        truePositive += 1
                        dataset.anadirRegla(dato, regla, True, round(calculoFinal, 2))
                        regla.datosCubre.append(dato)
                        regla.colorDatosCubre.append("blue")
                        regla.numDeDatosCubre.append(contDato)

                    else:
                        falseNegative += 1

                if (dato[len(regla.atributos)] != regla.clase):
                    if (contOcurrencias == contValoresAtributosRegla):
                        falsePositive += 1
                        dataset.anadirRegla(dato, regla, False, round(calculoFinal, 2))
                        regla.datosCubre.append(dato)
                        regla.colorDatosCubre.append("red")
                        regla.numDeDatosCubre.append(contDato)

                    else:
                        trueNegative += 1

            regla.realizarCalculos(
                truePositive, trueNegative, falsePositive, falseNegative, numDatos)

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
        for i in range(self.numEtiquetas):
            x0 = float(intervalo[i])
            x1 = float(intervalo[i+1])
            x2 = float(intervalo[i+2])

            if (valor < x1):
                calculo = ((valor-x0)*(y/(x1-x0)))
            if (valor > x1):
                calculo = ((x2-valor)*(y/(x2-x1)))

            if (calculo > pertenencia):
                pertenencia = calculo
                etiqueta = i
                calculo = -1.0

        return etiqueta, pertenencia
