from Manager import Manager
from lectura_ficheros.dataset import *
from lectura_ficheros.evolutivos import *
from utils.evaluacionReglasNoDiscretizado import *

if __name__ == "__main__":
    
    #pruebaD = lecturaDataset(r'C:\Users\padir\Desktop\experimentos\nmef SinDis\datasets\iris\iris-10-1tra.dat','nmeef')
    
    #pruebaD.lecturaFichero()

    #prueba = Evolutivos()
    #prueba.lecturaFichero(r'C:\Users\padir\Desktop\experimentos\nmef SinDis\results\NMEEF-SD.iris\result0e0SD.txt',pruebaD)

    #evaluador = evaluacionReglasNoDiscretizado()
    #evaluador.evaluarReglas(pruebaD, prueba.reglas)
    
    app = Manager()
    app.mainloop()