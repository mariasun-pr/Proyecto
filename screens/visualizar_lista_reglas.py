import tkinter as tk
import sys
from tkinter import filedialog
from utils import style
from screens.regla_screen import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from tkinter import filedialog


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
        inicioFrame.grid_columnconfigure(2, weight=1)

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
        #frame_canvas.grid_columnconfigure(2, weight=1)

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

        tk.Button(
            inicioFrame,
            text="Exportar",
            command=lambda: self.exportar(),
            **style.STYLE_BUTTON,
            font=("Arial", 18)
        ).grid(
            row=0,
            column=2,
            padx=15,
            pady=11,
            sticky=tk.E,
        )

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
        fig.set_size_inches(w=((plt.get_current_fig_manager().window.winfo_screenwidth()/2)/100)-0.35, h=6.5)

        XY = np.arange(0, 101, 1)
        ax.fill_between(XY, XY, facecolor='red', alpha=0.65)
        for regla in self.controller.reglas:
            ax.scatter(regla.fpr, regla.tpr, s=110)
            nombreSeparado = regla.nombre.split(' ')
            plt.annotate(
                "      "+nombreSeparado[0]+" "+nombreSeparado[1], (regla.fpr, regla.tpr))

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=infoReglaFrame)
        canvas.draw()

        # Add canvas to Tkinter window
        canvas.get_tk_widget().grid(
            row=len(self.controller.reglas),
            column=0,
            #columnspan=2,
            sticky=tk.NSEW,
            pady=13,
        )

        self.figGraf1 = fig

    def DibujarPiramidePoblacion(self, infoReglaFrame):
        fig, ax = plt.subplots()
        cont = 0
        fig.set_size_inches(w=((plt.get_current_fig_manager().window.winfo_screenwidth()/2)/100)-0.35, h=6.5)


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
            #columnspan=2,
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
            texto = "Ejemplo "+ str(contNumDatos+1) +": "+",".join(dato)
            entradaTabla.insert(tk.END, texto)
            entradaTabla.configure(state=tk.DISABLED, **
                                   style.STYLE_TEXT, relief=tk.GROOVE,)
            fila_tabla.append(entradaTabla.get())

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
            tabla.append(fila_tabla)
            # 50 el número de entradas de la tabla en una página.
            if (contNumDatos % 50 == 0 or contNumDatos == len(self.controller.dataset.datos)):
                # Guardar la tabla en una imagen
                fig = plt.figure(figsize=(8.27, 12), dpi=300)
                ax = fig.add_subplot(111)
                ax.axis('off')
                ax.table(cellText=tabla, cellLoc='center', loc='center')
                self.tablaDatos.append(fig)
                tabla = []

    def exportar(self):
        nombreFichero = self.exportacionGeneral()
        self.exportacionReglaIndividual(nombreFichero)
        self.ventanaNotificacion()

    def exportacionGeneral(self):
        #nombreFichero = "informacion_general_"+self.controller.nombreAlgoritmo+".pdf"
        nombreFichero = filedialog.asksaveasfile(defaultextension=".pdf", filetypes=[("PDF Files", ".pdf"),("All files", "*.*")],initialfile="informacion_general_"+self.controller.nombreAlgoritmo+".pdf")
        if nombreFichero:
            with PdfPages(nombreFichero.name) as pdf:
                pdf.savefig(self.figGraf1)
                pdf.savefig(self.figGraf2)
                for page in self.tablaDatos:
                    pdf.savefig(page)
            return nombreFichero

    def exportacionReglaIndividual(self, nombreFichero):
        nombre = nombreFichero.name.replace('.pdf','')
        nombre = nombre + "_reglas.pdf"
        if nombreFichero:
            with PdfPages(nombre) as pdf:
                for regla in self.controller.reglas:
                    regla.generarGraficos()
                    pdf.savefig(regla.nombreExportar)
                    pdf.savefig(regla.tablaContingencias)
                    pdf.savefig(regla.graficoPuntos)
                    pdf.savefig(regla.graficoBarra)
                    for page in regla.tablaDatos:
                        pdf.savefig(page)


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
        tk.Label(ventana, text="Ha finalizado la exportación", font=("Arial", 12)).pack(pady=10)
        
        # Configurar la ventana de notificación para que desaparezca en 3 segundos
        ventana.after(3000, ventana.destroy)
        
        # Mostrar la ventana de notificación
        ventana.deiconify()
