import tkinter as tk
import sys
from tkinter import filedialog
from constantes import style
from screens.regla_screen import *

class VisualizarReglas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller
        self.reglas = controller.reglas
        self.canvas = tk.Canvas

        self.hecho=False

    
    def setReglas(self, reglas):
        self.reglas = reglas

    def move_to_regla(self):
        self.controller.show_frame(VisualizarInfoRegla, self.hecho)
        if(not self.hecho):
            self.hecho=True

    def movement_mouse_wheel(self,event):
        if sys.platform == 'darwin': # for OS X # also, if platform.system() == 'Darwin':
            delta = event.delta
        else:                            # for Windows, Linux
            delta = -event.delta // 120   # event.delta is some multiple of 120
        
        self.canvas.yview_scroll(delta, "units")
    

    
    def init_widgets(self):
        inicioFrame = tk.Frame(self)
        inicioFrame.configure(background=style.COLOR_BACKGROUND,)
        inicioFrame.pack(
            side = tk.TOP,
            fill=tk.X,
            padx=20,
            pady=11,
   
        )
        tk.Button(
            inicioFrame,
            text=" ← Atrás",
            command= lambda: self.controller.get_frame("Importar"),
            **style.STYLE_BUTTON,
            font=("Arial",13)
        ).pack(
            side = tk.LEFT,
            padx=20,
            pady=11, 
        )
        tk.Label(
            inicioFrame, 
            text="Selecciona una regla para ver más información",
            justify=tk.CENTER,
            **style.STYLE #Desenpaqueta STYLE,
        ).pack(
            fill=tk.X,
            padx=20,
            pady=11,  
            side=tk.LEFT, 
        )
        
        reglasFrame = tk.Frame(self)
        reglasFrame.configure(background=style.COLOR_BACKGROUND,)
        reglasFrame.pack(
            side = tk.TOP,
            fill=tk.BOTH,
            padx=20,
            #pady=11,  
            expand= 1,

        )

        self.canvas = tk.Canvas(reglasFrame)

        scrollbar = tk.Scrollbar(reglasFrame, orient=tk.VERTICAL, command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=scrollbar.set, background=style.COLOR_BACKGROUND, borderwidth=0, highlightthickness=0)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion= self.canvas.bbox(tk.ALL)))

        frame_canvas=tk.Frame(self.canvas)
        frame_canvas.configure(background=style.COLOR_BACKGROUND)
        self.canvas.create_window((0,0),window=frame_canvas,anchor=tk.NW)
 

        #Para que funcione el scroll con la rueda del ratón en cualquier SO
        self.canvas.bind("<MouseWheel>", self.movement_mouse_wheel)
        self.canvas.bind("<Button-4>", self.movement_mouse_wheel)
        self.canvas.bind("<Button-5>", self.movement_mouse_wheel)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)




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




