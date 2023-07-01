import tkinter as tk
from tkinter import messagebox as MessageBox
from tkinter import filedialog
from utils import style
from screens.visualizar_lista_reglas import *
from lectura_ficheros.dataset import *
from lectura_ficheros.apriori import *
from lectura_ficheros.cn2 import *
from lectura_ficheros.sd import *
from lectura_ficheros.sd_map import *
from lectura_ficheros.evolutivos import *
from utils.evaluaciónReglas import *
from utils.evaluacionReglasNoDiscretizado import *
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
        if(nombreFichero != ""):
            self.filenameDatos.set(nombreFichero)
        print('Selected:', self.filenameDatos.get)

        if self.filenameDatos.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ" and self.filenameReglas.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ":            
            self.botonSiguiente.config(state=tk.NORMAL)
            self.leerFicheros()

    #Método para importat el conjunto de reglas
    def importarReglas(self):
        nombreFichero = tk.filedialog.askopenfilename()
        if(nombreFichero != ""):
            self.filenameReglas.set(nombreFichero)
        print('Selected:', self.filenameReglas.get)

        if self.filenameDatos.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ" and self.filenameReglas.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ":
            self.botonSiguiente.config(state=tk.NORMAL)
            self.leerFicheros()

    def init_widgets(self):
        self.crearCabecera()
        self.apartadoDatset()
        self.apartadoReglas()

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
        algoritmo, discretizado = self.leerCabeceraRegla(self.filenameReglas.get())       #Se obtiene el algoritmo que ha generado las reglas
        self.controller.nombreAlgoritmo = algoritmo

        dataset = lecturaDataset(self.filenameDatos.get(), algoritmo)
        salidaDataset = dataset.lecturaFichero(discretizado)
        if(self.comprobacionErroresLectura(algoritmo, salidaDataset)): #Hay fallos
            return

        self.controller.dataset = dataset
        # TODO: Añadir algoritmos aquí
        if(algoritmo == "apriori"):
            self.controller.reglas = self.algoritmos[Apriori].lecturaFichero(self.filenameReglas.get(), dataset)
        
        elif(algoritmo == "cn2"):
            self.controller.reglas = self.algoritmos[Cn2].lecturaFichero(self.filenameReglas.get(), dataset)

        elif(algoritmo == "sd"):
            self.controller.reglas = self.algoritmos[Sd].lecturaFichero(self.filenameReglas.get(), dataset)

        elif(algoritmo == "sd_map"):
            self.controller.reglas = self.algoritmos[SdMap].lecturaFichero(self.filenameReglas.get(), dataset)

        elif(algoritmo in ALGORITMOS_EVOLUTIVOS):
            self.controller.reglas = self.algoritmos[Evolutivos].lecturaFichero(self.filenameReglas.get(), dataset)        

        if(self.controller.reglas[0].numEtiquetas > 0):
            evaluador = evaluacionReglasNoDiscretizado()
            evaluador.evaluarReglas(dataset, self.controller.reglas)
        else:
            evaluador = evaluacionReglas()
            evaluador.evaluarReglas(dataset, self.controller.reglas)

    def comprobacionErroresLectura(self, algoritmo, salidaDataset):
        if(algoritmo == 'error'):
            MessageBox.showerror(
                "Error", "El fichero de reglas no es correcto")
            self.botonSiguiente.config(state=tk.DISABLED)
            return True

        if(algoritmo not in ALGORITMOS_VALIDOS):
            MessageBox.showerror(
                "Error", "El algoritmo no está registrado en la aplicación")
            self.botonSiguiente.config(state=tk.DISABLED)
            return True

        if(salidaDataset == "No discretizado"):
            MessageBox.showerror(
                "Error", "El algoritmo necesita el conjunto de datos discretizado")
            self.botonSiguiente.config(state=tk.DISABLED)
            return True
        
        elif(salidaDataset == "Formato incorrecto"):
            MessageBox.showerror(
                "Error", "El formato del contenido del archivo es incorrecto")
            self.botonSiguiente.config(state=tk.DISABLED)
            return True
        
        elif(salidaDataset == "Discretizado"):
            MessageBox.showwarning(
                "Warning", "El conjunto de datos está discretizado y el algoritmo no lo necesita")
            self.botonSiguiente.config(state=tk.DISABLED)
            return True


    #Inicialización de los algoritmos que lee la aplicación
    def definirAlgoritmos(self):
        self.algoritmos = {}
        for Alg in (Apriori, Cn2, Sd, SdMap, Evolutivos):  #! Añadir aquí los algoritmos que se vayan añadiendo
            algoritmo = Alg()
            self.algoritmos[Alg] = algoritmo

    #Método que obtiene el algoritmo que ha generado las reglas
    def leerCabeceraRegla(self, nombreFichero):
        fichero = open(nombreFichero)
        linea = fichero.readline()
        linea = linea.rstrip()
        algoritmo = linea.replace('@algorithm ', '')

        texto = fichero.read()
        if 'Rule' not in texto and 'RULE' not in texto:
            return "error", False

        if 'Number of labels: ' in texto:
            return algoritmo, False
        else:
            return algoritmo, True
        
    def crearCabecera(self):
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

    def apartadoDatset(self):
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

    def apartadoReglas(self):
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
        

