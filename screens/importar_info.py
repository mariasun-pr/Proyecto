import tkinter as tk
from tkinter import messagebox as MessageBox
from tkinter import filedialog
from utils import style
from screens.visualizar_lista_reglas import *
from lectura_ficheros.dataset import *
from lectura_ficheros.apriori import *
from lectura_ficheros.cn2 import *
from lectura_ficheros.sd import *
from utils.evaluaciónReglas import *
from utils.constantes import *


class Importar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller
        self.filenameDatos = tk.StringVar(self, "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ")
        self.filenameReglas = tk.StringVar(self, "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ")
        self.botonSiguiente = tk.Button(
            self,
            text="Siguiente →",
            command=self.move_to_visualizarReglas,
            **style.STYLE_BUTTON,
            font=style.FONT_BUTTON,
            state=tk.DISABLED,
        )
        self.hecho = False

        self.definirAlgoritmos()


    #Método que pasa a la siguiente pantalla (Visualizar lista reglas).
    def move_to_visualizarReglas(self):
        self.controller.show_frame(VisualizarReglas, False)
        if(not self.hecho):
            self.hecho = True

    #Método para importar el dataset
    def importarDatos(self):
        nombreFichero = tk.filedialog.askopenfilename()
        self.filenameDatos.set(nombreFichero)
        print('Selected:', self.filenameDatos.get)

        if self.filenameReglas.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ" and self.filenameReglas.get() != "":
            self.botonSiguiente.config(state=tk.NORMAL)
            self.leerFicheros()

    #Método para importat el conjunto de reglas
    def importarReglas(self):
        nombreFichero = tk.filedialog.askopenfilename()
        self.filenameReglas.set(nombreFichero)
        print('Selected:', self.filenameReglas.get)

        if self.filenameDatos.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ" and self.filenameDatos.get() != "":
            self.botonSiguiente.config(state=tk.NORMAL)
            self.leerFicheros()

    def init_widgets(self):
        #Título
        tk.Label(
            self,
            text="Importa los ficheros",
            justify=tk.CENTER,
            **style.STYLE  # Desenpaqueta STYLE,
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            padx=20,
            pady=11,
            sticky=tk.NSEW,
        )
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    # Importar conjunto de datos
        datosFrame = tk.Frame(self)
        datosFrame.configure(background=style.COLOR_BACKGROUND,)
        datosFrame.grid(
            row=1,
            column=0,
            columnspan=2,
            padx=20,
            pady=11,
            sticky=tk.NSEW,
        )
        datosFrame.grid_columnconfigure(0, weight=1)
        datosFrame.grid_columnconfigure(1, weight=1)

        tk.Label(
            datosFrame,
            textvariable=self.filenameDatos,
            **style.STYLE_TEXT,
            width=0,
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=11,
            sticky=tk.NSEW,
        )

        tk.Button(
            datosFrame,
            text="Elija el conjunto de datos",
            command=self.importarDatos,
            **style.STYLE_BUTTON,
            font=("Arial", 16)
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=11,
            sticky=tk.NS,
        )

    # Importar reglas
        reglasFrame = tk.Frame(self)
        reglasFrame.configure(background=style.COLOR_BACKGROUND,)
        reglasFrame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=20,
            pady=11,
            sticky=tk.NSEW,
        )
        reglasFrame.grid_columnconfigure(0, weight=1)
        reglasFrame.grid_columnconfigure(1, weight=1)

        tk.Label(
            reglasFrame,
            textvariable=self.filenameReglas,
            **style.STYLE_TEXT,
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=11,
            sticky=tk.NSEW,
            ipadx=0
        )
        tk.Button(
            reglasFrame,
            text="Elija las reglas",
            command=self.importarReglas,
            **style.STYLE_BUTTON,
            font=("Arial", 16)
        ).grid(
            row=0,
            column=1,
            padx=20,
            pady=11,
            sticky=tk.NS,
        )

        # Botón siguiente
        if self.filenameDatos.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ" and self.filenameReglas.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ":
            self.estadoBoton = tk.NORMAL
        self.botonSiguiente.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=20,
            pady=11,
            sticky=tk.N,
        )


    def leerFicheros(self):
        algoritmo = self.leerCabeceraRegla(self.filenameReglas.get())       #Se obtiene el algoritmo que ha generado las reglas

        if(algoritmo not in ALGORITMOS_VALIDOS):
            MessageBox.showerror(
                "Error", "El algoritmo no está registrado en la aplicación")
            self.botonSiguiente.config(state=tk.DISABLED)
            return

        dataset = lecturaDataset(self.filenameDatos.get(), algoritmo)
        if(dataset.lecturaFichero() == "No discretizado"):
            MessageBox.showerror(
                "Error", "El algoritmo necesita el conjunto de datos discretizado")
            self.botonSiguiente.config(state=tk.DISABLED)
            return
        elif(dataset.lecturaFichero() == "Formato incorrecto"):
            MessageBox.showerror(
                "Error", "El formato del contenido del archivo es incorrecto")
            self.botonSiguiente.config(state=tk.DISABLED)
            return

        # TODO: Añadir algoritmos aquí
        if(algoritmo == "apriori"):
            self.controller.reglas = self.algoritmos[Apriori].lecturaFichero(self.filenameReglas.get(), dataset)
        
        if(algoritmo == "cn2"):
            self.controller.reglas = self.algoritmos[Cn2].lecturaFichero(self.filenameReglas.get(), dataset)

        if(algoritmo == "sd"):
            self.controller.reglas = self.algoritmos[Sd].lecturaFichero(self.filenameReglas.get(), dataset)

        evaluador = evaluacionReglas()
        evaluador.evaluarReglas(dataset, self.controller.reglas)

    #Inicialización de los algoritmos que lee la aplicación
    def definirAlgoritmos(self):
        self.algoritmos = {}
        for Alg in (Apriori, Cn2, Sd):  #! Añadir aquí los algoritmos que se vayan añadiendo
            algoritmo = Alg()
            self.algoritmos[Alg] = algoritmo

    #Método que obtiene el algoritmo que ha generado las reglas
    def leerCabeceraRegla(self, nombreFichero):
        fichero = open(nombreFichero)
        linea = fichero.readline()
        linea = linea.rstrip()
        algoritmo = linea.replace('@algorithm ', '')
        return algoritmo
