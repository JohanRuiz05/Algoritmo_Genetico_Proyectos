import random
import time

# Se crea el cromosoma inicial segun las indicaciones del usuario

filasU = int (input ("Ingrese el número de proyectos a evaluar: "))
print ()
columnasU = int (input("Ingrese el número de hitos por proyecto: "))
print ()

def cromosomas ():

    global cromosomaInicial
    global listaHitosEsperados
    global listaSeleccion
    
    cromosomaInicial = []
    listaHitosEsperados = []
    listaSeleccion = []

    for j in range (filasU):
        cromosomaInicial.append ([])
        hitosEsperados = int (input("Ingrese el número de hitos que deberían estar cumplidos según el cronograma del proyecto "+(str(j+1))+ ": "))
        print ()
        listaHitosEsperados.append (hitosEsperados)
    
        for i in range (columnasU):
                
                a = int (input ("Añada el estado de cumplimiento del hito "+ (str(i+1)) +" del proyecto "+(str(j+1))+ ": "))
                print ()
                if (a == 0) or (a == 1):
                    cromosomaInicial[j].append (a)
                else:
                    print ("Número inválido, vuelve a intentarlo")
                    print ()
                    a = int (input ("Añada el estado de cumplimiento del hito "+ (str(i+1)) +" del proyecto "+(str(j+1))+ ": "))
                    print ()
                    if (a == 0) or (a == 1):
                        cromosomaInicial[j].append (a)
                    else:
                        print ("Número inválido, vuelve a intentarlo")
                        print ()
                        a = int (input ("Añada el estado de cumplimiento del hito "+ (str(i+1)) +" del proyecto "+(str(j+1))+ ": "))
                        print ()
                        cromosomaInicial[j].append (a)
                        
    return cromosomaInicial

# Determina x

def valorX ():

    global cromosomaInicial
    global listaX
    x = 0
    listaX = []

    for i in range (filasU):
        for j in range (columnasU):
            if cromosomaInicial[i][j] == 1:
                x+= 1

        listaX.append (x)

    listaXCop = listaX [:]

    for i in range (len (listaX)):
        if i == 0:
            listaX [i] = listaX [i]
        else:
            listaX [i] = listaX [i]- (listaXCop [(i-1)])

# Se reemplaza x en la ecuación hitos cumplidos/hitos esperados

def funcion ():

    global listaX
    global valorFuncion
    global listaHitosEsperados
    valorFuncion = []
    
    for i in range (filasU):
        x = float (listaX [i])
        f = (x/listaHitosEsperados[i])
        valorFuncion.append ("{:.4f}".format(f))

    return valorFuncion

# Se halla la función de aptitud de cada x del algoritmo, y después se establecen las probabilidades de elección

def aptitud ():

    global valorFuncion
    global valorProbSeleccion
    global aptitudTotal
    global valorAptitudIndividual
    valorAptitudIndividual = []
    aptitudTotal = 0
    listaApt = []
    valorProbSeleccion = []  
    
    for i in range (filasU):
        aptitudIndividual = 10 - abs (float(valorFuncion [i]))
        valorAptitudIndividual.append ("{:.4f}".format(aptitudIndividual))
        aptT = ((float (valorAptitudIndividual [i]))/2)
        listaApt.append (aptT)

    for j in range (filasU):
        aptT2 = listaApt[j]
        aptitudTotal += aptT2

    for k in range (filasU):
        probSeleccion = ((listaApt[k])/(aptitudTotal))
        valorProbSeleccion.append ("{:.6f}".format(float(probSeleccion)))
        
    return valorProbSeleccion

# Se realiza la selección por elitismo

def seleccion ():

    global valorProbSeleccion
    global listaTotal
    global cromosomaInicial
    global cromosomaSeleccionado
    global nuevaAptitud
    global seleccionClasificacion
    global valorProbCopia
    global valorProbSeleccion
    global listaSeleccion
    
    valorProbCopia = valorProbSeleccion [:]
    valorProbSeleccion.sort()
    valorProbSeleccion.reverse()
    
    contador1 = filasU
    nuevaAptitud = {}
    
    for i in range (filasU):
        seleccion = valorProbSeleccion [i]
        nuevaAptitud [contador1] = seleccion
        contador1 -= 1

    # Se añade a la lista todas las probabilidades y se repite el proceso
        
    for j in range (filasU):
            seleccionClasificacion = valorProbSeleccion [j]
            listaSeleccion.append (seleccionClasificacion)

    # En caso de que listaSeleccion solo tenga un elemento

    if len (listaSeleccion) == 1:
            listaSeleccion.append (seleccionClasificacion)
            listaSeleccion.append (seleccionClasificacion)
            listaSeleccion.append (seleccionClasificacion)
    
    return listaSeleccion

# Se corre el algoritmo genético para crear una nueva población 

def algoritmoGenetico():

    global cromosomaSeleccionado
    global nuevaPoblacion
    global valorProbSeleccion
    global valorProbCopia
    global cromosomaInicial
    global seleccionClasificacion

    nuevaPoblacion = []

    cromosomas ()
    valorX ()
    funcion ()
    aptitud ()
    seleccion ()

    # Se elige aleatoriamente una probabilidad de listaSeleccion
        
    seleccionClasificacion = listaSeleccion [random.randrange (0,((len(listaSeleccion))-1))]
    indice = valorProbCopia.index (seleccionClasificacion)
    cromosomaSeleccionado = cromosomaInicial [indice]
    
    indice2 = valorProbCopia.index (valorProbSeleccion[random.randrange(0,((len(valorProbSeleccion))-1))])
    nuevaPoblacion.append (cromosomaInicial [indice2])

    # Se repiten los procesos durante ese rango

    for i in range (filasU-1):
        nuevaPoblacion.append (cromosomaSeleccionado)
        valorX ()
        funcion ()
        aptitud ()
        seleccion ()

    nuevaPoblacion [0] = cromosomaInicial [valorProbCopia.index (valorProbSeleccion[0])]
    nuevaPoblacion [(len(nuevaPoblacion))-1] = cromosomaInicial [valorProbCopia.index (valorProbSeleccion[0])]
    nuevaPoblacion [random.randrange(1,((len(valorProbSeleccion))-2))] = cromosomaInicial [valorProbCopia.index (valorProbSeleccion[0])]
    
# Se repite el algoritmo hasta que supere determinado umbral de aptitud

def funcionamiento ():

    algoritmoGenetico ()

    global aptitudTotal
    global valorProbSeleccion
    global nuevaAptitud

    prueba = 0
    
    while prueba < 200:
        valorX ()
        funcion ()
        aptitud ()
        seleccion ()
        prueba += 1
        
    if prueba == 200:
    
        global valorProbSeleccion
        global valorProbCopia
        global valoresNuevaProb
        global nuevaPoblacion
        global listaSeleccion

        # Se encuentra la máxima y la segunda máxima probabilidad

        maxProbabilidad = max (listaSeleccion)
        segMaxProbabilidad = valorProbSeleccion [1]

        # Se reemplaza listaSeleccion para que aumente la posibilidad de selección de la esperada

        for i in range (int ((len(listaSeleccion))/1.5)):
            listaSeleccion [random.randrange (0,((len(listaSeleccion))-1))] = maxProbabilidad
        for j in range (int ((len(listaSeleccion))/30)):
            listaSeleccion [random.randrange (0,((len(listaSeleccion))-1))] = segMaxProbabilidad
           
        # Se elige el cromosoma

        seleccionClasificacion = listaSeleccion [random.randrange (0,((len(listaSeleccion))-1))]
        indice = valorProbCopia.index (seleccionClasificacion)
        cromosomaSeleccionado = cromosomaInicial [indice]
        
        print ("El proyecto " + (str(indice+1)) + " requiere la revisión por parte del gerente del proyecto")
        print ()
        print ("Johan Ruiz y Sebastian Sánchez")
        time.sleep (10)

funcionamiento ()

