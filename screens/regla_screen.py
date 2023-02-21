import tkinter as tk
from tkinter import ttk
from utils import style
from screens.visualizar_lista_reglas import *


class VisualizarInfoRegla(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller

        self.hecho = False

    def move_to_visualizarReglas(self):
        self.controller.get_frame("VisualizarReglas")

    def init_widgets(self):
        #self.grid_columnconfigure(0, weight=1)
        #self.grid_columnconfigure(1, weight=1)

        inicioFrame = tk.Frame(self)
        inicioFrame.configure(background=style.COLOR_BACKGROUND,)
        inicioFrame.pack(
            side = tk.TOP,
            fill=tk.X,
            padx=20,
            pady=11,
        )
        #inicioFrame.grid_columnconfigure(0, weight=1)
        #inicioFrame.grid_columnconfigure(1, weight=1)

        tk.Button(
            inicioFrame,
            text=" ← Atrás",
            command=lambda: self.controller.get_frame("VisualizarReglas"),
            **style.STYLE_BUTTON,
            font=("Arial", 13)
        ).pack(
            side = tk.LEFT,
            padx=20,
            pady=11, 
        )
        nombreRegla = tk.Label(
            inicioFrame,
            text=self.controller.reglaSeleccionada.nombre,
            justify=tk.CENTER,
            wraplength=2000,
            **style.STYLE_TITULO_REGLAS  # Desenpaqueta STYLE,
        )
        nombreRegla.pack(
            fill=tk.X,
            padx=20,
            pady=11,  
            side=tk.LEFT, 
        )

        infoReglaFrame = tk.Frame(self)
        infoReglaFrame.configure(background=style.COLOR_BACKGROUND,)
        infoReglaFrame.pack(
            side = tk.TOP,
            fill=tk.X,
            padx=20,
            pady=11,
   
        )
        infoReglaFrame.grid_columnconfigure(0, weight=1)
        infoReglaFrame.grid_columnconfigure(1, weight=1)

        self.dibujarTablaContingencias(infoReglaFrame)



    def dibujarTablaContingencias(self, infoReglaFrame):
        tp = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
            width=40,
        )
        tp.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
        )
        tp.insert(tk.END, "True positive (tp)")
        tp.configure(state=tk.DISABLED, **style.STYLE_TITULO_TABLA,relief=tk.GROOVE,)

        tpValor = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
        )
        tpValor.grid(
            row=1,
            column=0,
            sticky=tk.NSEW,
        )
        tpValor.insert(tk.END, str(self.controller.reglaSeleccionada.tp))
        tpValor.configure(state=tk.DISABLED, **style.STYLE_TEXT,relief=tk.GROOVE,)

        tn = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
        )
        tn.grid(
            row=2,
            column=0,
            sticky=tk.NSEW,
        )
        tn.insert(tk.END, "True negative (tn)")
        tn.configure(state=tk.DISABLED, **style.STYLE_TITULO_TABLA,relief=tk.GROOVE,)

        tnValor = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
        )
        tnValor.grid(
            row=3,
            column=0,
            sticky=tk.NSEW,
        )
        tnValor.insert(tk.END, str(self.controller.reglaSeleccionada.tn))
        tnValor.configure(state=tk.DISABLED, **style.STYLE_TEXT,relief=tk.GROOVE,)

        fp = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
            width=40,
        )
        fp.grid(
            row=0,
            column=1,
            sticky=tk.NSEW,
        )
        fp.insert(tk.END, "False positive (fp)")
        fp.configure(state=tk.DISABLED, **style.STYLE_TITULO_TABLA,relief=tk.GROOVE,)

        fpValor = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
        )
        fpValor.grid(
            row=1,
            column=1,
            sticky=tk.NSEW,
        )
        fpValor.insert(tk.END, str(self.controller.reglaSeleccionada.fp))
        fpValor.configure(state=tk.DISABLED, **style.STYLE_TEXT,relief=tk.GROOVE,)

        fn = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
        )
        fn.grid(
            row=2,
            column=1,
            sticky=tk.NSEW,
        )
        fn.insert(tk.END, "False negative (fn)")
        fn.configure(state=tk.DISABLED, **style.STYLE_TITULO_TABLA,relief=tk.GROOVE,)

        fnValor = tk.Entry(
            infoReglaFrame,
            justify=tk.CENTER,
        )
        fnValor.grid(
            row=3,
            column=1,
            sticky=tk.NSEW,
        )
        fnValor.insert(tk.END, str(self.controller.reglaSeleccionada.fn))
        fnValor.configure(state=tk.DISABLED, **style.STYLE_TEXT,relief=tk.GROOVE,)

