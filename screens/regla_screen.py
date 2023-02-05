import tkinter as tk
from tkinter import filedialog
from constantes import style

class VisualizarInfoRegla(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller


    def init_widgets(self):
        print("Hola")