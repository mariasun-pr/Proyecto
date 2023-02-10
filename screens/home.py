import tkinter as tk
from tkinter import filedialog
from constantes import style
from screens.importar_info import *


class Home(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller

        # self.init_widgets()

    def move_to_importar(self):
        self.controller.show_frame(Importar, False)

    def init_widgets(self):
        tk.Label(
            self,
            text="Visualizador de algoritmos SDRD",
            justify=tk.CENTER,
            **style.STYLE  # Desenpaqueta STYLE,
        ).pack(
            side=tk.TOP,
            fill=tk.X,
            padx=20,
            pady=11,
        )
        self.phtotoImage = tk.PhotoImage(file="./assets/escudo3.png")
        tk.Label(
            self,
            image=self.phtotoImage,
            bg=style.COLOR_BACKGROUND,
            height=175,
            width=131,
            justify=tk.CENTER,
        ).pack(
            side=tk.TOP,
            fill=tk.X,
            padx=20,
        )
        tk.Button(
            self,
            text="Nueva visualización",
            command=self.move_to_importar,
            **style.STYLE_BUTTON,
            font=style.FONT_BUTTON,
        ).pack(
            side=tk.TOP,
            padx=20,
            fill=tk.Y,
        )
