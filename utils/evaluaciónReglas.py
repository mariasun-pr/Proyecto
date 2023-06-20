class evaluacionReglas:

    def evaluarReglas(self, dataset, reglas):
        numDatos = len(dataset.datos)

        for regla in reglas:
            truePositive = 0
            trueNegative = 0
            falsePositive = 0
            falseNegative = 0
            contDato = 0
            for dato in dataset.datos:
                contDato+=1
                contOcurrencias = 0
                contValoresAtributosRegla = 0
                for i in range(len(regla.atributos)):
                    if (regla.atributos[i] != None):
                        contValoresAtributosRegla += 1

                        if (regla.operadores[i] == '=' and regla.atributos[i] == dato[i]):
                            contOcurrencias += 1

                        elif (regla.operadores[i] == '<>' and regla.atributos[i] != dato[i]):
                            contOcurrencias += 1

                        elif (regla.operadores[i] == '<' and dato[i] < regla.atributos[i]):
                            contOcurrencias += 1

                        elif (regla.operadores[i] == '>' and dato[i] > regla.atributos[i]):
                            contOcurrencias += 1

                        elif (regla.operadores[i] == '=>' and int(dato[i]) >= int(regla.atributos[i])):
                            contOcurrencias += 1

                        elif (regla.operadores[i] == '<=' and int(dato[i]) <= int(regla.atributos[i])):
                            contOcurrencias += 1

                if (dato[len(regla.atributos)] == regla.clase):
                    if (contOcurrencias == contValoresAtributosRegla):
                        truePositive += 1
                        dataset.anadirRegla(dato, regla, True)
                        regla.datosCubre.append(dato)
                        regla.colorDatosCubre.append("blue")
                        regla.numDeDatosCubre.append(contDato)
                    else:
                        falseNegative += 1

                if (dato[len(regla.atributos)] != regla.clase):
                    if (contOcurrencias == contValoresAtributosRegla):
                        falsePositive += 1
                        dataset.anadirRegla(dato, regla, False)
                        regla.datosCubre.append(dato)
                        regla.colorDatosCubre.append("red")
                        regla.numDeDatosCubre.append(contDato)
                    else:
                        trueNegative += 1

            regla.realizarCalculos(truePositive,trueNegative,falsePositive,falseNegative, numDatos)

        for regla in reglas:
            regla.mostrar()

        for dato in dataset.datos:
            print(dato)
            print("\n\n")
