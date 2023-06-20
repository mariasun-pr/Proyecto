from screens.visualizar_lista_reglas import *
import matplotlib.pyplot as plt
import numpy as np



class Regla:
    def __init__(self, valoresAtributos, clase, nombreRegla, operadores, numE):
        self.atributos = valoresAtributos
        self.clase = clase
        self.nombre = nombreRegla
        self.operadores = operadores
        self.datosCubre = []
        self.colorDatosCubre = []
        self.numDeDatosCubre = []
        self.numEtiquetas = numE

        self.graficoPuntos = None

        self.tp = 0
        self.tn = 0
        self.fp = 0
        self.fn = 0

        self.tpr = 0
        self.fpr = 0
        self.WRAccN = 0
        self.confianza = 0

    def mostrar(self):
        print("\n\n\n"+self.nombre)
        print(self.atributos)
        print(self.operadores)
        print("tp:" + str(self.tp))
        print("tn:" + str(self.tn))
        print("fp:" + str(self.fp))
        print("fn:" + str(self.fn))
        print("tpr:" + str(self.tpr))
        print("fpr:" + str(self.fpr))

    def generarGraficos(self):
        if(self.graficoPuntos == None):
            self.dibujarGraficoPuntos()

    def dibujarGraficoPuntos(self):
        fig, ax = plt.subplots()
        ax.set_xlim(-1, 101)
        ax.set_ylim(-1, 101)
        ax.set_xlabel('FPr')
        ax.set_ylabel('TPr')
        ax.set_title('TPr/FPr')
        fig.set_size_inches(w=(plt.get_current_fig_manager().window.winfo_screenwidth()/100)-1, h=6.5)

        XY = np.arange(0, 101, 1)
        ax.fill_between(XY, XY, facecolor='red', alpha=0.65)
        ax.scatter(self.fpr, self.tpr, s=110)
        plt.annotate("  TPr: "+ str(self.tpr)+"\n"+"  FPr: " + str(self.fpr),(self.fpr, self.tpr))

        self.graficoPuntos = fig

        plt.close()

    def realizarCalculos(self, truePositive, trueNegative, falsePositive, falseNegative, numDatos):
        self.tp = truePositive
        self.tn = trueNegative
        self.fp = falsePositive
        self.fn = falseNegative

        self.tpr = round(
            (truePositive / (truePositive + falseNegative))*100, 2)
        self.fpr = round(
            (falsePositive / (falsePositive + trueNegative))*100, 2)
        if(falsePositive + truePositive == 0):
            self.confianza = 0
        else:
            self.confianza = round(
                (truePositive / (falsePositive + truePositive))*100, 2)
        self.WRAccN = round(
            (((truePositive+falsePositive)/numDatos)*(self.confianza-(truePositive+falseNegative)/numDatos)), 2)

