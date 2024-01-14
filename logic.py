import math
import random
from sympy import symbols, lambdify

funcion = "(x**3 * sin(x))/100 + x**2 *cos(x)"

class Individuo:
    def __init__(self, id, binario, i, x, y):
        self.id = id
        self.binario = binario
        self.i = i
        self.x = round(x, 4)
        self.y = round(y, 4)
    def __str__(self):
        return f"ID: {self.id}, i: {self.i}, Binario: {self.binario}, X: {self.x}, Y: {self.y}"

class Data:
    num_bits_necesarios = 0
    rango = 0
    resolucion = 0
    limite_inferior = 0
    limite_superior = 0
    poblacion_inicial = 0
    poblacion_maxima = 0
    tipo_problema_value = ""
    poblacion_general = []
    prob_mutacion_ind = 0
    prob_mutacion_gen = 0

def calcular_funcion(funcion, valor_x):
    x = symbols('x')
    expresion = lambdify(x, funcion, 'numpy')
    resultado = expresion(valor_x)
    return resultado

def calcular_valor_x(limite_inferior, num_generado, resolucion):
    valor_x = limite_inferior + num_generado*resolucion
    return valor_x


def genetic_algorithm(data):
        
    Data.poblacion_inicial = int(data.p_inicial)
    Data.poblacion_maxima = int(data.p_max)
    Data.resolucion = float(data.res)
    Data.limite_inferior = float(data.lim_inf)
    Data.limite_superior = float(data.lim_sup)
    Data.prob_mutacion_ind = float(data.prob_ind)
    Data.prob_mutacion_gen = float(data.prob_gen)
    Data.tipo_problema_value = data.tipo_problema
    
    #Empezamos sacando los datos 
    Data.rango = Data.limite_superior - Data.limite_inferior
    num_saltos = Data.rango/Data.resolucion
    num_puntos = num_saltos + 1
    num_bits = int(math.log2(num_puntos) + 1)
    rango_numero= 2**num_bits #256
    Data.num_bits_necesarios = len(bin(rango_numero)[2:])
    
    inicializacion(rango_numero);


def inicializacion(rango_numero):
    for i in range(Data.poblacion_inicial):
        num_generado = (random.randint(0, rango_numero))
        num_generado_binario = (bin(num_generado)[2:]).zfill(Data.num_bits_necesarios)
        valor_x = calcular_valor_x(Data.limite_inferior, num_generado, Data.resolucion)
        valor_y = calcular_funcion(funcion, valor_x)
        individuo = Individuo(id=i+1, i=num_generado, binario=num_generado_binario, x=valor_x, y= valor_y)
        Data.poblacion_general.append(individuo)
    
    optimizacion()


def optimizacion():
    #Estrategia A3: (100 %) la población se ordena y particiona en dos, los individuos de la
    #partición con mejor aptitud se cruzan con algunos o todos los individuos.
    flag = True
    if Data.tipo_problema_value == "Minimizacion":
        flag = False
    # Se ordenan todos los individuos para posteriormente particionarlos
    individuos_ordenados = sorted(Data.poblacion_general, key=lambda x: x.y, reverse=flag)
    
    #Particionamos en dos elementos y separamos la mejor aptitud, y los de peor aptitud
    mitad = int(len(individuos_ordenados) / 2)
    particion_mejor_aptitud = individuos_ordenados[:mitad]
    particion_menor_aptitud = individuos_ordenados[mitad:]

    for individuo in individuos_ordenados:
        print(f"ID: {individuo.id}, i: {individuo.i}, Binario: {individuo.binario}, X: {individuo.x}, Y: {individuo.y}")

    print("Poblacion con mejor aptitud:")
    for individuo in particion_mejor_aptitud:
        print(individuo)
    
    print("Resto de poblacion")
    resto_poblacion = []
    for individuo in particion_menor_aptitud:
        print(individuo)
        resto_poblacion.append(individuo)
        
    nueva_poblacion = emparejamiento(resto_poblacion, particion_mejor_aptitud)


def emparejamiento(resto_poblacion, particion_mejor_aptitud):
    nueva_poblacion = []
    for individuo in resto_poblacion:
        nueva_poblacion.append(individuo)
    
    for individuo in particion_mejor_aptitud:
        nueva_poblacion.append(individuo)

    for mejor_individuo in particion_mejor_aptitud:
        for individuo in resto_poblacion:
            nuevo_individuo1, nuevo_individuo2 = cruza(mejor_individuo, individuo)
            nueva_poblacion.append(nuevo_individuo1)
            nueva_poblacion.append(nuevo_individuo2)

    for individuo in nueva_poblacion:
        print("Nueva poblacion es:", individuo)
    return nueva_poblacion




def cruza(mejor_individuo, individuo):
    #Estrategia C1: (90 %) Un punto de cruza aleatorio, para cada pareja a cruzar, de los posibles
    #puntos de cruza de los individuos se selecciona aleatoriamente la posición.
    punto_cruza = random.randint(1, Data.num_bits_necesarios -1)
    print("Punto de cruza", punto_cruza)
    parte1 = mejor_individuo.binario[:punto_cruza]
    parte2 = mejor_individuo.binario[punto_cruza:]
    parte3 = individuo.binario[:punto_cruza]
    parte4 = individuo.binario[punto_cruza:]
    
    nuevo_individuo1 = parte1 + parte4
    nuevo_individuo2 = parte3 + parte2
    
    print("Primer cruce de ", mejor_individuo.id,"a cruzar con:", individuo.id, "=", nuevo_individuo1)
    print("Segundo cruce de ", mejor_individuo.id,"a cruzar con:", individuo.id, "=", nuevo_individuo2)
    
    
    if((random.randint(1,100))/100 <= Data.prob_mutacion_ind):
        mutacion(nuevo_individuo1)
        
    if((random.randint(1,100))/100 <= Data.prob_mutacion_ind):
        mutacion(nuevo_individuo2)
    
    return nuevo_individuo1, nuevo_individuo2
    

def mutacion(individuo):
    #Estrategia M1: (100 %) Negación del bit
    #for i in individuo:
        if((random.randint(1,100))/100 <= Data.prob_mutacion_gen):
            print("Negación del bit")

def poda():
    print("hello")

