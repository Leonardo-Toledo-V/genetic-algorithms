import math
import random
import tkinter as tk
from sympy import symbols, lambdify
from graphs.graphic import generar_graficas
from video import generar_video
from graphs.graphic2 import generar_segunda_grafica

class Individuo:
    identificador = 0
    def __init__(self, binario, i, x, y):
        Individuo.identificador += 1
        self.id = Individuo.identificador
        self.binario = binario
        self.i = i
        self.x = round(x, 4)
        self.y = round(y, 4)
    def __str__(self):
        return f"ID: {self.id}, i: {self.i}, Binario: {self.binario}, X: {self.x}, Y: {self.y}"


class Data:
    rango_punto_cruza = 1
    rango = 0
    rango_numero = 0
    resolucion: 0
    resolucion_deseada = 0
    limite_inferior = 0
    limite_superior = 0
    poblacion_inicial = 0
    poblacion_maxima = 0
    tipo_problema_value = ""
    poblacion_general = []
    prob_mutacion_ind = 0
    prob_mutacion_gen = 0
    num_generaciones = 0
    generacion_actual = 0
    funcion = ""
    num_bits = 1


class Estadisticas:
    mejor_individuo = None
    peor_individuo = None
    promedio = None
    mejor_individuo_arreglo = []
    peor_individuo_arreglo = []
    promedio_arreglo = []
    generacion_arreglo = []

def vaciarDatos():
    Data.rango_punto_cruza = 1
    Data.rango = 0
    Data.rango_numero = 0
    Data.resolucion: 0
    Data.resolucion_deseada = 0
    Data.limite_inferior = 0
    Data.limite_superior = 0
    Data.poblacion_inicial = 0
    Data.poblacion_maxima = 0
    Data.tipo_problema_value = ""
    Data.poblacion_general = []
    Data.prob_mutacion_ind = 0
    Data.prob_mutacion_gen = 0
    Data.num_generaciones = 0
    Data.generacion_actual = 0
    Data.funcion = ""
    Data.num_bits = 1
    Estadisticas.mejor_individuo = None
    Estadisticas.peor_individuo = None
    Estadisticas.promedio = None
    Estadisticas.mejor_individuo_arreglo = []
    Estadisticas.peor_individuo_arreglo = []
    Estadisticas.promedio_arreglo = []
    Estadisticas.generacion_arreglo = []

def calcular_funcion(funcion, valor_x):
    x = symbols('x')
    expresion = lambdify(x, funcion, 'numpy')
    resultado = expresion(valor_x)
    return resultado


def calcular_valor_x(num_generado):
    if Data.limite_inferior >= Data.limite_superior:
        valor_x = Data.limite_superior + num_generado*Data.resolucion
        print(f"valor de x en primer if {valor_x}")
        return valor_x
    valor_x = Data.limite_inferior + num_generado*Data.resolucion
    print(f"valor de x en segundo if {valor_x}")
    return valor_x


def calcular_datos():
    Data.rango = Data.limite_superior - Data.limite_inferior
    num_saltos = Data.rango/Data.resolucion_deseada
    num_puntos = num_saltos + 1
    Data.num_bits = math.log2(abs(num_puntos))
    if Data.num_bits % 1 !=0:
        Data.num_bits =  math.ceil(math.ceil(Data.num_bits))
    else:
        Data.num_bits = int(Data.num_bits)
    Data.resolucion = Data.rango/((2**Data.num_bits))
    print(f"resolucion {Data.resolucion}")
    print(f"rango : {Data.rango}")
    print(f"num_bits : {Data.num_bits}")
    if Data.resolucion % 1 == 0:
        Data.resolucion =  int(Data.resolucion)
    else:
        Data.resolucion = round(Data.resolucion, 4)        
    print(f"resolucion {Data.resolucion}")
    Data.rango_numero= 2**Data.num_bits-1
    Data.rango_punto_cruza = len(bin(Data.rango_numero)[2:])    


def generar_primer_poblacion():
        for i in range(Data.poblacion_inicial):
            num_generado = random.randint(1, Data.rango_numero)
            num_generado_binario = format(num_generado, f"0{Data.num_bits}b")
            valor_x = calcular_valor_x(num_generado)
            valor_y = calcular_funcion(Data.funcion, valor_x)
            individuo = Individuo(i=num_generado, binario=num_generado_binario, x=valor_x, y= valor_y)
            Data.poblacion_general.append(individuo)
        for individuo in Data.poblacion_general:
            print(f"este es el individuo generado {individuo}")


def imprimir_mejor_individuo():
    mensaje = f"El mejor individuo es: \n{Estadisticas.mejor_individuo}\n\n Revisa la carpeta results/first-graph/video para ver el video de la evolución del fitness"
    ventana_alerta = tk.Tk()
    ventana_alerta.title("Felicidades")

    etiqueta_mensaje = tk.Label(ventana_alerta, text=mensaje)
    etiqueta_mensaje.pack(padx=10, pady=10)
    
    ventana_alerta.mainloop()

def genetic_algorithm(data):   
    vaciarDatos()
    Data.poblacion_inicial = int(data.p_inicial)
    Data.poblacion_maxima = int(data.p_max)
    Data.resolucion_deseada = float(data.res)
    Data.limite_inferior = float(data.lim_inf)
    Data.limite_superior = float(data.lim_sup)
    Data.prob_mutacion_ind = float(data.prob_ind)
    Data.prob_mutacion_gen = float(data.prob_gen)
    Data.tipo_problema_value = data.tipo_problema
    Data.num_generaciones = int(data.num_generaciones)
    Data.funcion = data.funcion
    
    #Calculamos los datos con los datos dados
    calcular_datos()
    
    # Generamos nuestra primer poblacion
    generar_primer_poblacion()
    
    #Bucle de optimización
    for generacion in range(1, Data.num_generaciones + 1):
        Data.generacion_actual= generacion
        optimizacion()
        print(f"Población en la generación :{Data.generacion_actual} ")
        for individuo in Data.poblacion_general:
            print(individuo)
        generar_estadisticas()
    generar_video(Data.num_generaciones)
    imprimir_mejor_individuo()



def optimizacion():
    #Estrategia A3: (100 %) la población se ordena y particiona en dos, los individuos de la
    #partición con mejor aptitud se cruzan con algunos o todos los individuos.
    
    flag = True
    if Data.tipo_problema_value == "Minimizacion":
        flag = False

    individuos_ordenados = sorted(Data.poblacion_general, key=lambda x: x.y, reverse=flag)
    
    mitad = int(len(individuos_ordenados) / 2)
    particion_mejor_aptitud = individuos_ordenados[:mitad]
    particion_menor_aptitud = individuos_ordenados[mitad:]
    
    resto_poblacion = []
    for individuo in particion_menor_aptitud:
        resto_poblacion.append(individuo)
    emparejamiento(resto_poblacion, particion_mejor_aptitud)


def emparejamiento(resto_poblacion, particion_mejor_aptitud):
    for mejor_individuo in particion_mejor_aptitud:
        for individuo in resto_poblacion:
            cruza(mejor_individuo, individuo)


def cruza(mejor_individuo, individuo):
    #Estrategia C1: (90 %) Un punto de cruza aleatorio, para cada pareja a cruzar, de los posibles
    #puntos de cruza de los individuos se selecciona aleatoriamente la posición.
    
    punto_cruza = random.randint(1, Data.rango_punto_cruza -1)
    
    parte1 = mejor_individuo.binario[:punto_cruza]
    parte2 = mejor_individuo.binario[punto_cruza:]
    parte3 = individuo.binario[:punto_cruza]
    parte4 = individuo.binario[punto_cruza:]
    
    nuevo_individuo1 = parte1 + parte4
    nuevo_individuo2 = parte3 + parte2
    
    if(random.randint(1,100))/100 <= Data.prob_mutacion_ind:
        nuevo_individuo1 = mutacion(nuevo_individuo1)
        
    if(random.randint(1,100))/100 <= Data.prob_mutacion_ind:
        nuevo_individuo2 = mutacion(nuevo_individuo2)
    
    guardar_nuevos_individuos(nuevo_individuo1, nuevo_individuo2)
    
    poda()

def mutacion(individuo):
    #Estrategia M1: (100 %) Negación del bit
    
    binario_separado = list(individuo)
    for i in range(len(binario_separado)):
        if (random.randint(1,100))/100 <= Data.prob_mutacion_gen:
            binario_separado[i] = '1' if binario_separado[i] == '0' else '0'
    nuevo_binario = ''.join(binario_separado)
    
    return nuevo_binario


def poda():
    #Estrategia P2: (90 %) Eliminación aleatoria asegurando mantener al mejor individuo de la
    #población
    
    conjunto_i = set()
    poblacion_sin_repetidos = []

    for individuo in Data.poblacion_general:
        if individuo.i not in conjunto_i:
            conjunto_i.add(individuo.i)
            poblacion_sin_repetidos.append(individuo)

    Data.poblacion_general = poblacion_sin_repetidos

    flag = True
    if Data.tipo_problema_value == "Minimizacion":
        flag = False
    individuos_ordenados = sorted(Data.poblacion_general, key=lambda x: x.y, reverse=flag)

    nueva_poblacion = [individuos_ordenados[0]]
    
    if len(individuos_ordenados) > 1:
        nueva_poblacion.extend(random.sample(individuos_ordenados[1:], min(len(individuos_ordenados)-1, Data.poblacion_maxima-1)))

    Data.poblacion_general = nueva_poblacion


def guardar_nuevos_individuos(individuo1, individuo2):
    
    numero_decimal1 = int(individuo1, 2)
    numero_decimal2 = int(individuo2, 2)
    if Data.limite_inferior >= Data.limite_superior:
        x1 = Data.limite_superior + numero_decimal1*Data.resolucion
        x2 = Data.limite_superior + numero_decimal2*Data.resolucion
    else:
        x1 = Data.limite_inferior + numero_decimal1*Data.resolucion
        x2 = Data.limite_inferior + numero_decimal2*Data.resolucion
    
    y1 = calcular_funcion(Data.funcion, x1)
    y2 = calcular_funcion(Data.funcion, x2)
    
    individuo1 = Individuo(i=numero_decimal1, binario=individuo1, x=x1, y= y1)
    individuo2 = Individuo(i=numero_decimal2, binario=individuo2, x=x2, y= y2)
    
    
    Data.poblacion_general.append(individuo1)
    Data.poblacion_general.append(individuo2)


def generar_estadisticas():
    
    if Data.tipo_problema_value == "Minimizacion":
        mejor_individuo = min(Data.poblacion_general, key=lambda x: x.y)
        peor_individuo = max(Data.poblacion_general, key=lambda x: x.y)
    else:
        mejor_individuo = max(Data.poblacion_general, key=lambda x: x.y)
        peor_individuo = min(Data.poblacion_general, key=lambda x: x.y)
    
    promedio = sum(individuo.y for individuo in Data.poblacion_general) / len(Data.poblacion_general)
    
    Estadisticas.mejor_individuo = mejor_individuo
    Estadisticas.peor_individuo = peor_individuo
    Estadisticas.promedio = promedio

    Estadisticas.mejor_individuo_arreglo.append(Estadisticas.mejor_individuo.y)
    Estadisticas.peor_individuo_arreglo.append(Estadisticas.peor_individuo.y)
    Estadisticas.promedio_arreglo.append(Estadisticas.promedio)
    Estadisticas.generacion_arreglo.append(Data.generacion_actual)
    
    valores_x = [individuo.x for individuo in Data.poblacion_general]
    valores_y = [individuo.y for individuo in Data.poblacion_general]
    if Data.tipo_problema_value == "Minimizacion":
        mejor_x = min([individuo.x for individuo in Data.poblacion_general])
        mejor_y = min([individuo.y for individuo in Data.poblacion_general])
        peor_x = max([individuo.x for individuo in Data.poblacion_general])
        peor_y = max([individuo.y for individuo in Data.poblacion_general])
    else:
        mejor_x = max([individuo.x for individuo in Data.poblacion_general])
        mejor_y = max([individuo.y for individuo in Data.poblacion_general])
        peor_x = min([individuo.x for individuo in Data.poblacion_general])
        peor_y = min([individuo.y for individuo in Data.poblacion_general])    
    generar_segunda_grafica(valores_x, valores_y,mejor_x, mejor_y, peor_x, peor_y, Data.generacion_actual, Data.limite_inferior, Data.limite_superior, Estadisticas.mejor_individuo_arreglo, Estadisticas.peor_individuo_arreglo)
        
    #generar_graficas(Estadisticas.mejor_individuo_arreglo, Estadisticas.peor_individuo_arreglo, Estadisticas.promedio_arreglo, Estadisticas.generacion_arreglo, Data.num_generaciones)
