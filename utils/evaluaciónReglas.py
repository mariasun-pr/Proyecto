class evaluacionReglas:

def evaluarReglas(self, dataset, reglas):

    for dato in dataset.datos:
        datoLimpio = dato.split(',')

        for regla in reglas:
            if(regla.clase == datoLimpio[len(datoLimpio)-1]):
                
