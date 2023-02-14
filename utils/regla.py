class Regla:
    def __init__(self, valoresAtributos, clase, nombreRegla, operadores):
        self.atributos = valoresAtributos
        self.clase = clase
        self.nombre = nombreRegla
        self.operadores = operadores

    def mostrar(self):
        print("\n\n\n"+self.nombre + "\n")
        print(self.clase + "\n")
        print(self.atributos)
        print(self.operadores)
