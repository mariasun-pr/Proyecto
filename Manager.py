import tkinter as tk
from utils import style
from screens.visualizar_lista_reglas import *
from screens.importar_info import *
from screens.home import *
from screens.regla_screen import *

#Manager tiene todas las funciones para las pantallas

class Manager(tk.Tk):
    
    reglas = []
    reglasSeleccionada = None
    dataset = None
    nombreAlgoritmo = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Visualizador algoritmos SD")
        # Obtener el ancho y alto de la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        alto_pantalla = self.winfo_screenheight()

        # Establecer el tamaño de la ventana
        self.geometry("%dx%d+0+0" % (ancho_pantalla, alto_pantalla-75))

        self.container = tk.Frame(self) #parent del home. Contiene los frames
        self.container.pack(
            side = tk.TOP,
            fill = tk.BOTH,
            expand=True
        )
        self.container.configure(background=style.COLOR_BACKGROUND)
        self.container.grid_columnconfigure (0,weight=1) #Se está definiendo que el container tenga una sola fila y una sola columna
        self.container.grid_rowconfigure(0,weight=1)#El peso lo que ocupa la columna respecto el otro

        self.frames = {} #Diccionario de clase
        for F in (Home, Importar, VisualizarReglas, VisualizarInfoRegla): #!Modificar aquí para añadir vistas
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW) 
        self.show_frame(Home, False)

    def show_frame(self, container, hecho):
        frame = self.frames[container]
        if(not hecho):
            frame.init_widgets()
        frame.tkraise()
    
    def get_frame(self, nombreVentana):
        if nombreVentana == "Importar":
            self.frames[VisualizarReglas].destroy()
            frame = VisualizarReglas(self.container, self)
            self.frames[VisualizarReglas] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)

            self.show_frame(Importar, True)

        elif nombreVentana == "VisualizarReglas":
            self.frames[VisualizarInfoRegla].destroy()
            frame = VisualizarInfoRegla(self.container, self)
            self.frames[VisualizarInfoRegla] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW)
            
            self.show_frame(VisualizarReglas, True)
