from Manager import Manager
from lectura_ficheros.dataset import *

if __name__ == "__main__":
    prueba = lecturaDataset(r'C:\Users\padir\Desktop\p\p\datasets\Fayyad-D.iris\Fayyad-D.iris-10-1tra.dat','cn2')
    prueba = lecturaDataset(r'C:\Users\padir\Desktop\p\p\datasets\iris\iris-10-1tra.dat','cn2')
    
    prueba.lecturaFichero()

    #app = Manager()
    #app.mainloop()


