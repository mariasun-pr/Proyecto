from Manager import Manager
from lectura_ficheros.dataset import *
from lectura_ficheros.apriori import *

if __name__ == "__main__":
    pruebaD = lecturaDataset(r'C:\Users\padir\Desktop\appendicitis\appendicitis.dat','fhg')
    #pruebaD = lecturaDataset(r'C:\Users\padir\Desktop\p\p\datasets\iris\iris-10-1tra.dat','cn2')
    
    pruebaD.lecturaFichero()

    prueba = LecturaApriori()
    prueba.lecturaFichero(r'D:\padir\ESCRITORIO\Mariasun\Universidad\4º\TFG\Keel\SD\apriori\appendicitis-exit.txt',pruebaD)

    #app = Manager()
    #app.mainloop()


