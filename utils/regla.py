class Regla:
    def __init__(self, valoresAtributos, clase, nombreRegla, operadores):
        self.atributos = valoresAtributos
        self.clase = clase
        self.nombre = nombreRegla
        self.operadores = operadores

        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

    def mostrar(self):
        print("\n\n\n"+self.nombre)
        #print(self.clase + "\n")
        print(self.atributos)
        print(self.operadores)
        print("tp:" + str(self.tp))
        print("tn:" + str(self.tn))
        print("fp:" + str(self.fp))
        print("fn:" + str(self.fn))
