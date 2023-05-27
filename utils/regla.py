import tkinter as tk
from utils import style
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

        self.nombreExportar = None
        self.graficoPuntos = None
        self.graficoBarra = None
        self.tablaDatos = []
        self.tablaContingencias = None

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
        # print(self.clase + "\n")
        print(self.atributos)
        print(self.operadores)
        print("tp:" + str(self.tp))
        print("tn:" + str(self.tn))
        print("fp:" + str(self.fp))
        print("fn:" + str(self.fn))
        print("tpr:" + str(self.tpr))
        print("fpr:" + str(self.fpr))

        #print(self.datosCubre[0])

    def generarGraficos(self):
        if(self.graficoBarra == None):
            self.generarNombre()
            self.dibujarTablaContingencias()
            self.dibujarGraficoPuntos()
            #self.dibujarGraficoPiramide()
            self.dibujarTablaDatos()

    def generarNombre(self):
        # Crear un objeto de figura de matplotlib
        fig = plt.figure()

        # Agregar texto a la figura
        fig.text(0.5, 0.5, self.nombre, ha='center', va='center')
        self.nombreExportar = fig

        plt.close()


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

    def dibujarGraficoPiramide(self):
        fig, ax = plt.subplots()
        ax.barh(0, self.tpr, align='center')
        ax.barh(0, -self.fpr, align='center')
        fig.set_size_inches(w=(plt.get_current_fig_manager().window.winfo_screenwidth()/100)-1, h=6.5)

        ax.set_xticks(np.arange(-100, 101, 20))
        ax.set_xticklabels(['100', '80', '60', '40', '20',
                           '0', '20', '40', '60', '80', '100'])
        plt.ylim(0, 0.2)
        ax.annotate("FPr: " + str(self.fpr)+ "    " + "TPr: " + str(self.tpr), (-35, 0.175), size=13)

        ax.set_xlabel('FPr y TPr')
        ax.set_title('Pirámide FPr/TPr')
        plt.yticks([])

        self.graficoBarra = fig

        plt.close()

    def dibujarTablaDatos(self):
        contNumDatos = 0
        tabla = []

        for dato in self.datosCubre:
            tabla.append(dato)
            contNumDatos+=1

            # 50 el número de entradas de la tabla en una página.
            if (contNumDatos % 50 == 0 or contNumDatos == len(self.datosCubre)):
                # Guardar la tabla en una imagen
                fig = plt.figure(figsize=(8.27, 12), dpi=300)
                if(contNumDatos == 50 or contNumDatos == len(self.datosCubre)):
                    fig.text(0.5, 0.85, "Tabla de los datos que cubre la regla", ha='center', va='center', fontsize = 20)
                ax = fig.add_subplot(111)
                ax.axis('off')
                ax.table(cellText=tabla, loc='center')
                self.tablaDatos.append(fig)
                tabla = []
                plt.close()

    def dibujarTablaContingencias(self):
        tabla = [["True positive (tp)","False positive (fp)"],
                 [str(self.tp),str(self.fp)],
                 ["True negative (tn)","False negative (fn)"],
                 [str(self.tn),str(self.fn)]]

        fig = plt.figure(figsize=(8, 5), dpi=300)
        fig.text(0.5, 0.65, "Tabla de contingencias", ha='center', va='center', fontsize= 20)
        ax = fig.add_subplot(111)
        ax.axis('off')
        table = ax.table(cellText=tabla, cellLoc='center', loc='center')
        table[0,0].set_facecolor('lightgray')
        table[0,1].set_facecolor('lightgray')
        table[2,0].set_facecolor('lightgray')
        table[2,1].set_facecolor('lightgray')
        self.tablaContingencias = fig
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
        self.confianza = round(
            (truePositive / (falsePositive + truePositive))*100, 2)
        self.WRAccN = round(
            (((truePositive+falsePositive)/numDatos)*(self.confianza-(truePositive+falseNegative)/numDatos)), 2)

