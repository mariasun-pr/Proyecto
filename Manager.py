import tkinter as tk
from constantes import style
from screens.visualizar_lista_reglas import *
from screens.importar_info import *
from screens.home import *
from screens.regla_screen import *

#Manager tiene todas las funciones para las pantallas

class Manager(tk.Tk):
    
    reglas = ["jfjdf\n","jdfhjf\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n","dfiuhiufh\n"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Visualizador algoritmos SD")
        self.geometry("1000x500")
        container = tk.Frame(self) #parent del home. Contiene los frames
        container.pack(
            side = tk.TOP,
            fill = tk.BOTH,
            expand=True
        )
        container.configure(background=style.COLOR_BACKGROUND)
        container.grid_columnconfigure (0,weight=1) #Se está definiendo que el container tenga una sola fila y una sola columna
        container.grid_rowconfigure(0,weight=1)#El peso lo que ocupa la columna respecto el otro

        self.frames = {} #Diccionario de clase
        for F in (Home, Importar, VisualizarReglas, VisualizarInfoRegla): #Modificar aquí para añadir pantallas
            frame = F(container, self)
            frame.init_widgets()
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky=tk.NSEW) 
        self.show_frame(Home)

    def show_frame(self, container):
        frame = self.frames[container]
        frame.tkraise()
       # self.container.update()
    
    def get_frame(self, nombreVentana):
        if nombreVentana == "Importar":
            self.show_frame(Importar)
        elif nombreVentana == "VisualizarReglas":
            return self.frames[VisualizarReglas]
