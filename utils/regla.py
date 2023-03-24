import matplotlib.pyplot as plt
import numpy as np


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

        self.tpr = 0
        self.fpr = 0

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

        """
        #!GRÁFICO DE PUNTOS
        plt.xlim(-1, 101)
        plt.ylim(-1, 101)
        plt.xlabel('FPr')
        plt.ylabel('TPr')
        plt.title('Scatter Plot')

        XY = np.arange(0, 101, 1)
        plt.fill_between(XY, XY, facecolor='red', alpha=0.65)
        plt.scatter(self.fpr, self.tpr, s=110)
        plt.annotate("  TPr: "+ str(self.tpr)+"\n"+"  FPr: " + str(self.fpr),(self.fpr, self.tpr))
       
         """

        #!PIRÁMIDE DE POBLACIÓN
""""
        fig, ax = plt.subplots()
        XY = np.arange(0, 101, 1)
        ax.barh(0, self.tpr, align='center')
        ax.barh(0, -self.fpr, align='center')

        ax.set_xticks(np.arange(-100, 101, 20))
        ax.set_xticklabels(['100', '80', '60', '40', '20',
                           '0', '20', '40', '60', '80', '100'])
        plt.ylim(0, 0.2)
        ax.annotate("FPr: " + str(self.fpr)+ "    " + "TPr: " + str(self.tpr), (-35, 0.175), size=13)

        ax.set_xlabel('FPr y TPr')
        ax.set_ylabel('TPr')
        ax.set_title('Scatter Plot')
        plt.yticks([])

        plt.show()
"""

""""
        age_groups = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60+']
        male_population = [100, 200, 300, 400, 500, 600, 700]
        female_population = [800, 700, 600, 500, 400, 300, 200]

        # Create population pyramid
        fig, ax = plt.subplots()

        ax.barh(1, male_population)
        ax.barh(1, female_population)

        ax.set_xlabel('Population')
        ax.set_ylabel('Age Group')
        ax.set_title('Population Pyramid')

        plt.show()"""
