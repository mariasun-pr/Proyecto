import tkinter as tk
import sys
from tkinter import filedialog
from utils import style
from screens.regla_screen import *


class VisualizarReglas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller
        self.reglas = controller.reglas
        self.canvas = tk.Canvas

        self.hecho = False

    def setReglas(self, reglas):
        self.reglas = reglas

    def move_to_regla(self, regla):
        self.controller.reglaSeleccionada = regla
        self.controller.show_frame(VisualizarInfoRegla, False)
        if(not self.hecho):
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
        
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox(tk.ALL)))

        frame_canvas = tk.Frame(self.canvas)
        frame_canvas.configure(background=style.COLOR_BACKGROUND)
        frame_canvas.grid_columnconfigure(0, weight=1)
        self.canvas.create_window((0, 0), window=frame_canvas, anchor=tk.N)

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
            )
            cont += 1
