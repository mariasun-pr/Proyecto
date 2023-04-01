import tkinter as tk
import sys
from tkinter import filedialog
from utils import style
from screens.regla_screen import *
import sys
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np


class VisualizarReglas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller
        self.canvas = tk.Canvas

        self.hecho = False

    def move_to_regla(self, regla):
        self.controller.reglaSeleccionada = regla
        self.controller.show_frame(VisualizarInfoRegla, False)
        if (not self.hecho):
            self.hecho = True

    def movement_mouse_wheel(self, event):
        if sys.platform == 'darwin':  # for OS X # also, if platform.system() == 'Darwin':
            delta = event.delta
        else:                            # for Windows, Linux
            delta = -event.delta // 120   # event.delta is some multiple of 120

        self.canvas.yview_scroll(delta, "units")

    def init_widgets(self):
        inicioFrame = tk.Frame(self)
        inicioFrame.configure(background=style.COLOR_BACKGROUND,)
        inicioFrame.pack(
            side=tk.TOP,
            fill=tk.X,
            padx=20,
            pady=11,
        )
        tk.Button(
            inicioFrame,
            text=" ← Atrás",
            command=lambda: self.controller.get_frame("Importar"),
            **style.STYLE_BUTTON,
            font=("Arial", 13)
        ).grid(
            row=0,
            column=0,
            padx=15,
            pady=11,
            sticky=tk.W,
        )

        tk.Label(
            inicioFrame,
            text="Selecciona una regla para ver más información",
            justify=tk.CENTER,
            **style.STYLE  # Desenpaqueta STYLE,
        ).grid(
            row=0,
            column=1,
            pady=11,
            sticky=tk.W,
        )
        inicioFrame.grid_columnconfigure(0, weight=1)
        inicioFrame.grid_columnconfigure(1, weight=1)

        reglasFrame = tk.Frame(self)
        reglasFrame.configure(background=style.COLOR_BACKGROUND,)
        reglasFrame.pack(
            side=tk.TOP,
            fill=tk.BOTH,
            padx=20,
            # pady=11,
            expand=1,
        )
        reglasFrame.grid_columnconfigure(0, weight=1)
        reglasFrame.grid_rowconfigure(0, weight=1)

        self.canvas = tk.Canvas(reglasFrame)

        scrollbar = tk.Scrollbar(
            reglasFrame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=scrollbar.set,
                              background=style.COLOR_BACKGROUND,
                              borderwidth=0,
                              highlightthickness=0)



        frame_canvas = tk.Frame(self.canvas)
        frame_canvas.configure(background=style.COLOR_BACKGROUND)
        frame_canvas.grid_columnconfigure(0, weight=1)
        frame_canvas.grid_columnconfigure(1, weight=1)
        self.canvas.create_window((1, 1), window=frame_canvas, anchor=tk.N)

        # Para que funcione el scroll con la rueda del ratón en cualquier SO
        self.canvas.bind("<MouseWheel>", self.movement_mouse_wheel)
        self.canvas.bind("<Button-4>", self.movement_mouse_wheel)
        self.canvas.bind("<Button-5>", self.movement_mouse_wheel)

        self.canvas.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            pady=20,
        )

        scrollbar.grid(
            row=0,
            column=1,
            sticky=tk.NS,
            pady=20,
        )

        self.AccesoReglaIndividual(frame_canvas)
        self.DibujarGraficoPuntos(frame_canvas)
        self.DibujarPiramidePoblacion(frame_canvas)
        self.TablaDatosCubreRegla(frame_canvas)

        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox(tk.ALL)))

    def AccesoReglaIndividual(self, frame_canvas):
        cont = 0
        for regla in self.controller.reglas:
            tk.Button(
                frame_canvas,
                text=regla.nombre,
                command=lambda r=regla: self.move_to_regla(r),
                **style.STYLE_BUTTON,
                font=("Arial", 14),
                justify=tk.LEFT,
            ).grid(
                column=0,
                row=cont,
                padx=10,
                sticky=tk.NSEW,
                columnspan=2
            )
            cont += 1

    def DibujarGraficoPuntos(self, infoReglaFrame):
        fig, ax = plt.subplots()
        ax.set_xlim(-1, 101)
        ax.set_ylim(-1, 101)
        ax.set_xlabel('FPr')
        ax.set_ylabel('TPr')
        ax.set_title('TPr/FPr')
        fig.set_size_inches(w=(plt.get_current_fig_manager().window.winfo_screenwidth()/100)-1, h=6.5)

        XY = np.arange(0, 101, 1)
        ax.fill_between(XY, XY, facecolor='red', alpha=0.65)
        for regla in self.controller.reglas:
            ax.scatter(regla.fpr, regla.tpr, s=110)
            nombreSeparado = regla.nombre.split(' ')
            plt.annotate("      "+nombreSeparado[0]+" "+nombreSeparado[1], (regla.fpr, regla.tpr))

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=infoReglaFrame)
        canvas.draw()

        # Add canvas to Tkinter window
        canvas.get_tk_widget().grid(
            row=len(self.controller.reglas),
            column=0,
            columnspan=2,
            sticky=tk.NSEW,
            pady=13,
        )

    def DibujarPiramidePoblacion(self, infoReglaFrame):
        fig, ax = plt.subplots()
        cont = 0
        fig.set_size_inches(w=(plt.get_current_fig_manager().window.winfo_screenwidth()/100)-1, h=6.5)
        for regla in self.controller.reglas:
            ax.barh(cont, regla.tpr, align='center', color='#00B6FF')
            ax.barh(cont, -regla.fpr, align='center', color='#CB3234')
            nombreSeparado = regla.nombre.split(' ')
            ax.annotate(nombreSeparado[0]+" "+nombreSeparado[1], (-10, cont), size=11)
            #ax.annotate("FPr: " + str(regla.fpr)+ "         " + "TPr: " + str(regla.tpr), (-35, cont-0.2), size=11)
            cont+=1

        ax.set_xticks(np.arange(-100, 101, 20))
        ax.set_xticklabels(['100', '80', '60', '40', '20',
                           '0', '20', '40', '60', '80', '100'])

        ax.set_xlabel('FPr y TPr')
        ax.set_title('Pirámide FPr/TPr')
        plt.yticks([])

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=infoReglaFrame)
        canvas.draw()

        # Add canvas to Tkinter window
        canvas.get_tk_widget().grid(
            row=len(self.controller.reglas)+1,
            column=0,
            columnspan=2,
            sticky=tk.NSEW,
            pady=13,
        )

    def TablaDatosCubreRegla(self, infoReglaFrame):
        tituloTabla = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
        )
        tituloTabla.grid(
            row=len(self.controller.reglas)+2,
            column=0,
            sticky=tk.NSEW,
            columnspan=2
        )
        tituloTabla.insert(tk.END, "Reglas que cubren a cada dato")
        tituloTabla.configure(state=tk.DISABLED, **
                     style.STYLE_TITULO_TABLA, relief=tk.GROOVE,)
        
        cont = len(self.controller.reglas)+3
        for dato in self.controller.dataset.datos:
            entradaTabla = tk.Entry(
                infoReglaFrame,
                justify=tk.CENTER,
            )
            entradaTabla.grid(
                row=cont,
                column=0,
                sticky=tk.NSEW,
            )
            entradaTabla.insert(tk.END, dato)
            entradaTabla.configure(state=tk.DISABLED, **
                          style.STYLE_TEXT, relief=tk.GROOVE,)
            
            entradaReglas = tk.Entry(
                infoReglaFrame,
                justify=tk.CENTER,
            )
            entradaReglas.grid(
                row=cont,
                column=1,
                sticky=tk.NSEW,
            )
            texto = self.controller.dataset.reglasCubren[self.controller.dataset.datos.index(dato)]
            if(texto == None):
                texto = ''
            entradaReglas.insert(tk.END, texto)
            entradaReglas.configure(state=tk.DISABLED, **
                          style.STYLE_TEXT, relief=tk.GROOVE,)
            
            cont+=1
