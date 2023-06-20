import tkinter as tk
import sys
from tkinter import filedialog
from utils import style
from screens.regla_screen import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.backends.backend_svg
import numpy as np
from utils.constantes import CustomHovertip
import zipfile


class VisualizarReglas(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.configure(background=style.COLOR_BACKGROUND)
        self.controller = controller
        self.canvas = tk.Canvas

        self.hecho = False

        self.figGraf1 = None
        self.figGraf2 = None
        self.tablaDatos = []

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
        self.crearCabecera()
        frame_canvas = self.crearInfoReglas()

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
        fig.set_size_inches(
            w=((plt.get_current_fig_manager().window.winfo_screenwidth()/2)/100)-0.35, h=6.5)

        XY = np.arange(0, 101, 1)
        ax.fill_between(XY, XY, facecolor='red', alpha=0.65)
        for regla in self.controller.reglas:
            ax.scatter(regla.fpr, regla.tpr, s=110)
            nombreSeparado = regla.nombre.split(' ')
            plt.annotate(
                "    "+nombreSeparado[0]+" "+nombreSeparado[1], (regla.fpr, regla.tpr))

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=infoReglaFrame)
        canvas.draw()

        # Add canvas to Tkinter window
        canvas.get_tk_widget().grid(
            row=len(self.controller.reglas),
            column=0,
            # columnspan=2,
            sticky=tk.NSEW,
            pady=13,
        )

        self.figGraf1 = fig

    def DibujarPiramidePoblacion(self, infoReglaFrame):
        fig, ax = plt.subplots()
        cont = 0
        fig.set_size_inches(
            w=((plt.get_current_fig_manager().window.winfo_screenwidth()/2)/100)-0.35, h=6.5)

        for regla in self.controller.reglas:
            ax.barh(cont, regla.tpr, align='center', color='#1F77B4')
            ax.barh(cont, -regla.fpr, align='center', color='#FF7F0E')
            nombreSeparado = regla.nombre.split(' ')
            ax.annotate(nombreSeparado[0]+" " +
                        nombreSeparado[1], (-10, cont), size=11)
            cont += 1

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
            row=len(self.controller.reglas),
            column=1,
            sticky=tk.NSEW,
            pady=13,
        )

        self.figGraf2 = fig

    def TablaDatosCubreRegla(self, infoReglaFrame):
        tablaFrame = tk.Frame(infoReglaFrame)
        tablaFrame.configure(background=style.COLOR_BACKGROUND,)
        tablaFrame.grid(
            row=len(self.controller.reglas)+1,
            column=0,
            sticky=tk.NSEW,
            columnspan=2
        )
        tablaFrame.grid_columnconfigure(0, weight=1)
        tablaFrame.grid_columnconfigure(1, weight=1)
        tablaFrame.grid_columnconfigure(2, weight=1)

        tituloTabla = tk.Entry(
            tablaFrame,
            justify=tk.CENTER,
        )
        tituloTabla.grid(
            row=0,
            column=0,
            sticky=tk.NSEW,
            columnspan=3
        )
        tituloTabla.insert(tk.END, "Reglas que cubren a cada dato")
        tituloTabla.configure(state=tk.DISABLED, **
                              style.STYLE_TITULO_TABLA, relief=tk.GROOVE,)

        cont = 1
        contNumDatos = 0
        tabla = []
        for dato in self.controller.dataset.datos:
            fila_tabla = []
            entradaTabla = tk.Entry(
                tablaFrame,
                justify=tk.CENTER,
            )
            entradaTabla.grid(
                row=cont,
                column=0,
                sticky=tk.NSEW,
            )
            texto = "Ejemplo " + \
                str(contNumDatos+1) + ": " + \
                    self.controller.dataset.datosFormateados[contNumDatos]
            entradaTabla.insert(tk.END, texto)
            entradaTabla.configure(state=tk.DISABLED, **
                                   style.STYLE_TEXT, relief=tk.GROOVE,)
            fila_tabla.append(entradaTabla.get())

            infoDelDato = "Ejemplo: " + str(contNumDatos+1) + "\n"
            for i in range(len(self.controller.dataset.atributos)):
                infoDelDato = infoDelDato + \
                    self.controller.dataset.atributos[i]+": "+dato[i]+"\n"
            infoDelDato += "Class: " + dato[len(dato)-1]
            CustomHovertip(entradaTabla, text=infoDelDato, hover_delay=75)

            entradaReglasBien = tk.Entry(
                tablaFrame,
                justify=tk.CENTER,
            )
            entradaReglasBien.grid(
                row=cont,
                column=1,
                sticky=tk.NSEW,
            )
            texto = self.controller.dataset.reglasCubrenBien[self.controller.dataset.datos.index(
                dato)]
            if (texto == None):
                texto = ''
            entradaReglasBien.insert(tk.END, texto)
            entradaReglasBien.configure(state=tk.DISABLED, **
                                    style.STYLE_REGLA_BIEN, relief=tk.GROOVE,)
            fila_tabla.append(entradaReglasBien.get())

            entradaReglasMal = tk.Entry(
                tablaFrame,
                justify=tk.CENTER,
            )
            entradaReglasMal.grid(
                row=cont,
                column=2,
                sticky=tk.NSEW,
            )
            texto = self.controller.dataset.reglasCubrenMal[self.controller.dataset.datos.index(
                dato)]
            if (texto == None):
                texto = ''
            entradaReglasMal.insert(tk.END, texto)
            entradaReglasMal.configure(state=tk.DISABLED, **
                                    style.STYLE_REGLA_MAL, relief=tk.GROOVE,)
            fila_tabla.append(entradaReglasMal.get())

            cont += 1
            contNumDatos += 1

    def ventanaNotificacion(self):
        ventana = tk.Toplevel()
        ventana.title("Notificación")  # Establecer el título de la ventana
        ventana.geometry("300x100")
        ventana.resizable(False, False)

        # Obtener la resolución de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()

        # Calcular la posición del Toplevel en el centro
        x = int((screen_width - ventana.winfo_reqwidth()) / 2)
        y = int((screen_height - ventana.winfo_reqheight()) / 2)

        # Establecer la posición del Toplevel en el centro
        ventana.geometry("+{}+{}".format(x, y))

        # Crear un label con el mensaje de notificación
        tk.Label(ventana, text="Ha finalizado la exportación",
                 font=("Arial", 12)).pack(pady=10)

        # Configurar la ventana de notificación para que desaparezca en 3 segundos
        ventana.after(3000, ventana.destroy)

        # Mostrar la ventana de notificación
        ventana.deiconify()

    def ventanaCabecera(self):
        ventana = tk.Toplevel()
        # Establecer el título de la ventana
        ventana.title("Cabecera del dataset")

        # Crear labels con la información de la cabecera
        tk.Label(ventana, text="Cabecera del dataset",
                 font=("Arial", 18, "bold")).pack(pady=10)
        tk.Label(ventana, text=self.controller.dataset.cabecera,
                 font=("Arial", 14)).pack()

        # Actualizar las dimensiones de la ventana
        ventana.update_idletasks()

        # Obtener el ancho y alto de la ventana
        window_width = ventana.winfo_width()
        window_height = ventana.winfo_height()

        # Obtener el ancho y alto de la pantalla
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()

        # Calcular la posición x, y para que la ventana esté centrada
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Establecer la posición del Toplevel en el centro
        ventana.geometry("+{}+{}".format(x, y))

        # Mostrar la ventana de notificación
        ventana.deiconify()

    def exportar2(self):
        nombreFichero = filedialog.asksaveasfile(defaultextension=".zip", filetypes=[("ZIP Files", ".zip"), (
            "All files", "*.*")], initialfile="informacion_general_"+self.controller.nombreAlgoritmo+".zip")
        if nombreFichero:
            self.figGraf1.savefig('graficaPuntos.svg', format='svg')
            self.figGraf2.savefig('graficaPiramide.svg', format='svg')
            self.exportarToLatexGeneral()
            self.exportarReglas()

            with zipfile.ZipFile(nombreFichero.name, 'w') as zipf:
                # Agregar los archivos SVG al ZIP
                zipf.write('graficaPuntos.svg')
                zipf.write('graficaPiramide.svg')

                zipf.write('infoGeneral.tex')
                zipf.write('infoReglas.tex')
                zipf.close()

            self.ventanaNotificacion()

    def exportarToLatexGeneral(self):
        # Crear el código LaTeX inicial para el documento
        latex_code = "\\documentclass{article}\n"
        latex_code +="\\usepackage{graphicx}\n"
        latex_code +="\\usepackage{longtable}\n"
        latex_code +="\\usepackage{tabularx}\n"
        latex_code +="\\usepackage{svg}\n"
        latex_code +="\\usepackage{geometry}\n"
        latex_code +="\\geometry{left=2cm}\n"
        latex_code += "\\begin{document}\n"
        
        latex_code += "\\section*{Cabecera del dataset}\n"

        # Agregar el texto encima de la tabla
        latex_code += self.controller.dataset.cabecera.replace("\n", " \\\\\n")

        # Agregar los gráficos encima de la tabla
        latex_code += "\\section*{Graficas}\n"
        latex_code += "\\begin{figure}[htbp]\n"
        latex_code += "\\centering\n"
        latex_code += "\\includesvg[width=1.2\linewidth]{graficaPuntos.svg}\n"
        latex_code += "\\end{figure}\n\n"
        latex_code += "\\begin{figure}[htbp]\n"
        latex_code += "\\includesvg[width=1.2\linewidth]{graficaPiramide.svg}\n"
        latex_code += "\\end{figure}\n\n"

        latex_code += "\\newpage\n"
        latex_code += "\\section*{Tabla de las reglas que cubren a los datos}\n"
        # Agregar la tabla
        latex_code += "\\begin{longtable}{|c|c|c|c|c|c|c|c|}\n"
        latex_code += "\\hline\n"

        # Recorrer las filas de la tabla
        for i in range(-1, len(self.controller.dataset.datos)):
            # Recorrer las columnas de cada fila
            if (i == -1):
                latex_code += "Ej & " + self.controller.dataset.atributos[0] + " & " + self.controller.dataset.atributos[1] + " & ... & Clase & Cubren BIEN & Cubren MAL"
            else:
                dato = self.controller.dataset.datos[i]
                for col in range(0, 4):
                    if(col == 0):
                        value = str(i+1) + " & "
                    elif(col == 1):
                        texto = self.controller.dataset.datosFormateados[i].split(", ")
                        value+= texto[0]+" & "+texto[1]+" & "+texto[3]+" & " +texto[4]+" & "
                    elif(col == 2):
                        texto = " & "
                        if(self.controller.dataset.reglasCubrenBien[self.controller.dataset.datos.index(dato)] != None):
                            texto = self.controller.dataset.reglasCubrenBien[self.controller.dataset.datos.index(dato)] + " & "
                        value += texto
                    elif(col == 3):
                        texto = ""
                        if(self.controller.dataset.reglasCubrenMal[self.controller.dataset.datos.index(dato)] != None):
                            texto = self.controller.dataset.reglasCubrenMal[self.controller.dataset.datos.index(dato)]
                        value += texto
                    # Agregar el valor al código LaTeX
                latex_code += value
            
            # Agregar el fin de la fila
            latex_code += " \\\\ \\hline\n"
        
        # Agregar el fin de la tabla
        latex_code += "\\end{longtable}\n"
        
        # Cerrar el documento LaTeX
        latex_code += "\\end{document}"
        
        # Guardar el código LaTeX en un archivo
        with open("infoGeneral.tex", "w") as file:
            file.write(latex_code)

    def exportarReglas(self):
        latex_code = "\\documentclass{article}\n"
        latex_code +="\\usepackage{graphicx}\n"
        latex_code +="\\usepackage{longtable}\n"
        latex_code +="\\usepackage{tabularx}\n"
        latex_code +="\\usepackage{geometry}\n"
        latex_code +="\\geometry{left=2cm}\n"
        latex_code += "\\begin{document}\n"

        for regla in self.controller.reglas:
            latex_code += "\\section*{" + regla.nombre + "}\n"
            latex_code += "\\subsection*{Tabla de contingencias}\n"
            latex_code += "\\begin{longtable}{|c|c|}\n"
            latex_code += "\\hline\n"
            latex_code += "True positive (tp) & False positive(fp)" 
            latex_code += " \\\\ \\hline\n"
            latex_code += str(regla.tp) + " & " + str(regla.fp)
            latex_code += " \\\\ \\hline\n" 
            latex_code += "True negative (tn) & False negative(fn)" 
            latex_code += " \\\\ \\hline\n"
            latex_code += str(regla.tn) + " & " + str(regla.fn)
            latex_code += " \\\\ \\hline\n" 
            latex_code += "\\end{longtable}\n"

            latex_code += "\\subsection*{Tabla de medidas (\%)}\n"
            latex_code += "\\begin{longtable}{|c|c|}\n"
            latex_code += "\\hline\n"
            latex_code += "Conf & WRAccN" 
            latex_code += " \\\\ \\hline\n"
            latex_code += str(regla.confianza) + " & " + str(regla.WRAccN)
            latex_code += " \\\\ \\hline\n" 
            latex_code += "True positive rate (TPr) & False positive(FPr)" 
            latex_code += " \\\\ \\hline\n"
            latex_code += str(regla.tpr) + " & " + str(regla.fpr)
            latex_code += " \\\\ \\hline\n" 
            latex_code += "\\end{longtable}\n"

            latex_code += "\\subsection*{Tabla de los datos que cubre}\n"
            latex_code += "\\begin{longtable}{|c|}\n"
            latex_code += "\\hline\n"
            contadorDatos = 0
            for dato in regla.datosCubre:
                latex_code +="Ejemplo "+ str(regla.numDeDatosCubre[contadorDatos]) +": "+",".join(dato)
                latex_code += " \\\\ \\hline\n" 
                contadorDatos+=1
            latex_code += "\\end{longtable}\n"
            latex_code += "\\newpage\n"
                # Cerrar el documento LaTeX
        latex_code += "\\end{document}"
        
        # Guardar el código LaTeX en un archivo
        with open("infoReglas.tex", "w") as file:
            file.write(latex_code)

    def crearCabecera(self):
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
            sticky=tk.NSEW,
        )

        tk.Button(
            inicioFrame,
            text="Exportar",
            command=lambda: self.exportar2(),
            **style.STYLE_BUTTON,
            font=("Arial", 18)
        ).grid(
            row=0,
            column=3,
            padx=15,
            pady=11,
            sticky=tk.E,
        )

        tk.Button(
            inicioFrame,
            text="Info del dataset",
            command=lambda: self.ventanaCabecera(),
            **style.STYLE_BUTTON,
            font=("Arial", 18)
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=11,
            sticky=tk.E,
        )

        inicioFrame.grid_columnconfigure(0, weight=1)
        inicioFrame.grid_columnconfigure(1, weight=1)
        inicioFrame.grid_columnconfigure(2, weight=1)
        inicioFrame.grid_columnconfigure(3, weight=1)

    def crearInfoReglas(self):
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

        return frame_canvas
            

