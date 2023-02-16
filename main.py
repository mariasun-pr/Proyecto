from Manager import Manager
from lectura_ficheros.dataset import *
from lectura_ficheros.apriori import *
from utils.evaluaciónReglas import *

if __name__ == "__main__":
    pruebaD = lecturaDataset(r'C:\Users\padir\Desktop\p\p\datasets\Fayyad-D.iris\Fayyad-D.iris-10-1tra.dat','fhg')
    #pruebaD = lecturaDataset(r'C:\Users\padir\Desktop\p\p\datasets\iris\iris-10-1tra.dat','cn2')
    
    pruebaD.lecturaFichero()

    prueba = LecturaApriori()
    prueba.lecturaFichero(r'C:\Users\padir\Desktop\p\p\results\Fayyad-D.Apriori-SD.iris\result0e0.txt',pruebaD)

    evaluador = evaluacionReglas()
    evaluador.evaluarReglas(pruebaD, prueba)

    #app = Manager()
    #app.mainloop()


