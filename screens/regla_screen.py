import tkinter as tk
from tkinter import filedialog
from constantes import style
from screens.visualizar_lista_reglas import *


class VisualizarInfoRegla(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller

        self.hecho = False

    def move_to_visualizarReglas(self):
        self.controller.get_frame("VisualizarReglas")

    def on_label_resize(self,  event):
        event.widget["wraplength"] = event.width

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
            command=lambda: self.controller.get_frame("VisualizarReglas"),
            **style.STYLE_BUTTON,
            font=("Arial", 13)
        ).pack(
            side=tk.LEFT,
            padx=20,
            pady=11,
        )
        nombreRegla = tk.Label(
            inicioFrame,
            textvariable=self.controller.nombre_regla_a_mostrar,
            justify=tk.CENTER,
            wraplength=2000,
            **style.STYLE_TITULO_REGLAS  # Desenpaqueta STYLE,
        )
        nombreRegla.bind("<Configure>", self.on_label_resize)
        nombreRegla.pack(
            fill=tk.X,
            padx=20,
            pady=11,
            side=tk.LEFT,
        )