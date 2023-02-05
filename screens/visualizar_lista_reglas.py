import tkinter as tk
from tkinter import filedialog
from constantes import style
from screens.regla_screen import *

class VisualizarReglas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller
        self.reglas = controller.reglas

    
    def setReglas(self, reglas):
        self.reglas = reglas

    def move_to_regla(self):
        self.controller.show_frame(VisualizarInfoRegla)

    
    def init_widgets(self):
        inicioFrame = tk.Frame(self)
        inicioFrame.configure(background=style.COLOR_BACKGROUND,)
        inicioFrame.pack(
            side = tk.TOP,
            fill=tk.X,
            padx=20,
            pady=11,
            expand=True    
        )
        tk.Button(
            inicioFrame,
            text=" ← Atrás",
            command= lambda: self.controller.get_frame("Importar"),
            **style.STYLE_BUTTON,
            font=("Arial",12)
        ).pack(
            side = tk.LEFT,
            padx=20,
        )
        tk.Label(
            inicioFrame, 
            text="Selecciona la regla para ver más información",
            justify=tk.CENTER,
            **style.STYLE #Desenpaqueta STYLE,
        ).pack(
            fill=tk.X,
            padx=20,
            pady=11,  
            side=tk.LEFT 
        )
        
        reglasFrame = tk.Frame(inicioFrame)
        reglasFrame.configure(background=style.COLOR_BACKGROUND,)
        reglasFrame.pack(
            #side = tk.LEFT,
            fill=tk.BOTH,
            padx=20,
            pady=11,  
            expand= 1  
        )

        canvas = tk.Canvas(reglasFrame)

        scrollbar = tk.Scrollbar(reglasFrame, orient=tk.VERTICAL, command=canvas.yview)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox(tk.ALL)))

        frame_canvas=tk.Frame(canvas)
        canvas.create_window((0,0),window=frame_canvas,anchor=tk.NW)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        #reglasFrame.config(yscrollcommand=scrollbar.set)


        print(self.controller.reglas)
        for regla in self.controller.reglas:
            tk.Button(
                frame_canvas,
                text=regla,
                command=self.move_to_regla,
                **style.STYLE_BUTTON,
                font=("Arial",14),
                state= tk.NORMAL,
            ).pack(
                side = tk.TOP,
                padx=20,
            )




