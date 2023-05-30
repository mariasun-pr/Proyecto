from idlelib.tooltip import Hovertip
import tkinter as tk

ALGORITMOS_NO_CONTINUOS = ["apriori","cn2","sd","sd_map", ]

ALGORITMOS_VALIDOS = ALGORITMOS_NO_CONTINUOS
ALGORITMOS_EVOLUTIVOS = ["mesdif", "nmeef", "sdiga"]
ALGORITMOS_VALIDOS += ALGORITMOS_EVOLUTIVOS

class CustomHovertip(Hovertip):
    def showcontents(self):
        label = tk.Label(
            self.tipwindow, text=f'{self.text}', justify=tk.LEFT,
            fg="black", relief=tk.SOLID, borderwidth=1, bg="#FDFD96",
            font=("Arial", 12)
            )
        label.pack()
        x, y = self.get_position()
        root_x = self.anchor_widget.winfo_rootx() + 20*x
        root_y = self.anchor_widget.winfo_rooty() - 3*y
        self.tipwindow.wm_geometry("+%d+%d" % (root_x, root_y))