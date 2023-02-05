import tkinter as tk
from tkinter import filedialog
from constantes import style
from screens.visualizar_lista_reglas import *


class Importar(tk.Frame):
    def __init__(self,parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller
        self.filenameDatos = tk.StringVar(self,"ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ")
        self.filenameReglas = tk.StringVar(self,"ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ")
        self.botonSiguiente = tk.Button(
                                self,
                                text="Siguiente →",
                                command=self.move_to_visualizarReglas,
                                **style.STYLE_BUTTON,
                                font=style.FONT_BUTTON,
                                state= tk.DISABLED,
                            )

        #self.init_widgets()

    def move_to_visualizarReglas(self):
        self.controller.show_frame(VisualizarReglas)
    
    def importarDatos(self):
        nombreFichero = tk.filedialog.askopenfilename()
        self.filenameDatos.set(nombreFichero)
        print('Selected:', self.filenameDatos.get)
        self.leerFichero(nombreFichero)
        if self.filenameReglas.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ" and self.filenameReglas.get() != "" :
            self.botonSiguiente.config(state=tk.NORMAL)

    def importarReglas(self):
        nombreFichero = tk.filedialog.askopenfilename()
        self.filenameReglas.set(nombreFichero)
        print('Selected:', self.filenameReglas.get)
        
        if self.filenameDatos.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ" and self.filenameDatos.get() != "":
            self.botonSiguiente.config(state=tk.NORMAL)

        self.controller.reglas=self.leerFichero(nombreFichero)


    def init_widgets(self):
        tk.Label(
            self, 
            text="Importa los ficheros",
            justify=tk.CENTER,
            **style.STYLE #Desenpaqueta STYLE,
        ).pack(
            side = tk.TOP,
            fill=tk.X,
            padx=20,
            pady=11,   
        )
    #Importar conjunto de datos
        datosFrame = tk.Frame(self)
        datosFrame.configure(background=style.COLOR_BACKGROUND,)
        datosFrame.pack(
            side = tk.TOP,
            fill=tk.X,
            padx=20,
            pady=11,    
        )
        tk.Label(
            datosFrame,
            textvariable= self.filenameDatos,
            **style.STYLE_TEXT,
            width=0,
        ).pack(            
            side = tk.LEFT,
            padx=20,
            pady=11, 
            fill=tk.X, 
        )
        tk.Button(
            datosFrame,
            text="Elija el conjunto de datos",
            command= self.importarDatos,
            **style.STYLE_BUTTON,
            font=("Arial",16)
        ).pack(
            side = tk.LEFT,
            padx=20,
        )

    #Importar reglas
        reglasFrame = tk.Frame(self)
        reglasFrame.configure(background=style.COLOR_BACKGROUND,)
        reglasFrame.pack(
            side = tk.TOP,
            fill=tk.BOTH,
            padx=20,
            pady=11,
        )
        tk.Label(
            reglasFrame,
            textvariable= self.filenameReglas,
            **style.STYLE_TEXT,
        ).pack(
            side=tk.LEFT,
            fill=tk.X,
            padx=20,
            pady=11,
        )
        tk.Button(
            reglasFrame,
            text="Elija las reglas",
            command= self.importarReglas,
            **style.STYLE_BUTTON,
            font=("Arial",16)
        ).pack(
            side = tk.LEFT,
            padx=20,
        )

        #Botón siguiente
        if self.filenameDatos.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ" and self.filenameReglas.get() != "ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ":
            self.estadoBoton = tk.NORMAL
        self.botonSiguiente.pack(
            side=tk.TOP,
            padx=20
        )


    def leerFichero(self, nombreFichero):
        fichero = open(nombreFichero)
        lineas = fichero.readlines()
        print(lineas)
        return lineas




