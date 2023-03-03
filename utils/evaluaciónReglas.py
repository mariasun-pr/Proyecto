class evaluacionReglas:

    def evaluarReglas(self, dataset, reglas):

        for regla in reglas:
            truePositive = 0
            trueNegative = 0
            falsePositive = 0
            falseNegative = 0

            for dato in dataset.datos:
                contOcurrencias = 0
                contValoresAtributosRegla = 0

                for i in range(len(regla.atributos)):
                    if(regla.atributos[i] != None):
                        contValoresAtributosRegla += 1

                        if(regla.operadores[i] == '=' and regla.atributos[i] == dato[i]):
                            contOcurrencias += 1

                        elif(regla.operadores[i] == '<>' and regla.atributos[i] != dato[i]):
                            contOcurrencias += 1

                        elif(regla.operadores[i] == '<' and dato[i] < regla.atributos[i]):
                            contOcurrencias += 1

                        elif(regla.operadores[i] == '>' and dato[i] > regla.atributos[i]):
                            contOcurrencias += 1

                        elif(regla.operadores[i] == '=>' and int(dato[i]) >= int(regla.atributos[i])):
                            contOcurrencias += 1

                        elif(regla.operadores[i] == '<=' and int(dato[i]) <= int(regla.atributos[i])):
                            contOcurrencias += 1

                if(dato[len(regla.atributos)] == regla.clase):
                    if(contOcurrencias == contValoresAtributosRegla):
                        truePositive += 1
                        dataset.anadirRegla(dato, regla)
                    else:
                        falseNegative += 1

                if(dato[len(regla.atributos)] != regla.clase):
                    if(contOcurrencias == contValoresAtributosRegla):
                        falsePositive += 1
                    else:
                        trueNegative += 1

            regla.tp = truePositive
            regla.tn = trueNegative
            regla.fp = falsePositive
            regla.fn = falseNegative

        for regla in reglas:
            regla.mostrar()

        for dato in dataset.datos:
            print(dato)
            print(dataset.reglasCubren[dataset.datos.index(dato)])
            print("\n\n")
