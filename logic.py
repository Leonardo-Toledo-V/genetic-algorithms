import math
import random
from sympy import symbols, lambdify

funcion = "(x**3 * sin(x))/100 + x**2 *cos(x)"

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
    num_generaciones = 0
    mejor_individuo = []

class Estadisticas:
    promedio: []
    menor: []
    mayor: []



def calcular_funcion(funcion, valor_x):
    x = symbols('x')
    expresion = lambdify(x, funcion, 'numpy')
    resultado = expresion(valor_x)
    return resultado

def calcular_valor_x(num_generado):
    valor_x = Data.limite_inferior + num_generado*Data.resolucion
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
    Data.num_generaciones = int(data.num_generaciones)
    
    for generacion in range(1, Data.num_generaciones + 1):
        print(f"\nGeneración {generacion}:")
        # Empezamos sacando los datos 
        Data.rango = Data.limite_superior - Data.limite_inferior
        num_saltos = Data.rango/Data.resolucion
        num_puntos = num_saltos + 1
        num_bits = int(math.log2(num_puntos) + 1)
        rango_numero= 2**num_bits -1 #256
        Data.num_bits_necesarios = len(bin(rango_numero)[2:])
    
        inicializacion(rango_numero, generacion);
    for generacion, mejor_individuo in Data.mejor_individuo:
        print(f"Generación {generacion}: ID: {mejor_individuo.id}, i: {mejor_individuo.i}, Binario: {mejor_individuo.binario}, X: {mejor_individuo.x}, Y: {mejor_individuo.y}")


def inicializacion(rango_numero, generacion):
    for i in range(Data.poblacion_inicial):
        num_generado = (random.randint(0, rango_numero))
        num_generado_binario = (bin(num_generado)[2:]).zfill(Data.num_bits_necesarios)
        valor_x = calcular_valor_x(num_generado)
        valor_y = calcular_funcion(funcion, valor_x)
        individuo = Individuo(i=num_generado, binario=num_generado_binario, x=valor_x, y= valor_y)
        Data.poblacion_general.append(individuo)
        
    mejor_individuo_actual = optimizacion()
    Data.mejor_individuo.append((generacion, mejor_individuo_actual))




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

    #for individuo in individuos_ordenados:
    #    print(f"ID: {individuo.id}, i: {individuo.i}, Binario: {individuo.binario}, X: {individuo.x}, Y: {individuo.y}")

    #print("Poblacion con mejor aptitud:")
    #for individuo in particion_mejor_aptitud:
    #    print(individuo)
    
    #print("Resto de poblacion")
    resto_poblacion = []
    for individuo in particion_menor_aptitud:
    #    print(individuo)
        resto_poblacion.append(individuo)
        
    emparejamiento(resto_poblacion, particion_mejor_aptitud)
    return particion_mejor_aptitud[0]


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




def cruza(mejor_individuo, individuo):
    #Estrategia C1: (90 %) Un punto de cruza aleatorio, para cada pareja a cruzar, de los posibles
    #puntos de cruza de los individuos se selecciona aleatoriamente la posición.
    punto_cruza = random.randint(1, Data.num_bits_necesarios -1)
    #print("Punto de cruza", punto_cruza)
    parte1 = mejor_individuo.binario[:punto_cruza]
    parte2 = mejor_individuo.binario[punto_cruza:]
    parte3 = individuo.binario[:punto_cruza]
    parte4 = individuo.binario[punto_cruza:]
    
    nuevo_individuo1 = parte1 + parte4
    nuevo_individuo2 = parte3 + parte2
    
    #print("Primer cruce de ", mejor_individuo.id,"a cruzar con:", individuo.id, "sin mutar es =", nuevo_individuo1)
    #print("Segundo cruce de ", mejor_individuo.id,"a cruzar con:", individuo.id, " sin mutar es =", nuevo_individuo2)
    
    
    if(random.randint(1,100))/100 <= Data.prob_mutacion_ind:
        nuevo_individuo1 = mutacion(nuevo_individuo1)
        
    if(random.randint(1,100))/100 <= Data.prob_mutacion_ind:
        nuevo_individuo2 = mutacion(nuevo_individuo2)
    
    
    #print("individuo 1 despues de la mutacion: ", nuevo_individuo1)
    #print("individuo 2 despues de la mutacion: ", nuevo_individuo2)
    
    
    guardar_nuevos_individuos(nuevo_individuo1, nuevo_individuo2)
    
    poda()
    
    return nuevo_individuo1, nuevo_individuo2
    

def mutacion(individuo):
    #Estrategia M1: (100 %) Negación del bit
    binario_separado = list(individuo)
    for i in range(len(binario_separado)):
        if (random.randint(1,100))/100 <= Data.prob_mutacion_gen:
            binario_separado[i] = '1' if binario_separado[i] == '0' else '0'
    nuevo_binario = ''.join(binario_separado)
    return nuevo_binario

def poda():
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

    if len(individuos_ordenados) > Data.poblacion_maxima:
        Data.poblacion_general = individuos_ordenados[:Data.poblacion_maxima]

    print("Población después de la poda:")
    for individuo in Data.poblacion_general:
        print(individuo)



def guardar_nuevos_individuos(individuo1, individuo2):
    

    numero_decimal1 = int(individuo1, 2)
    numero_decimal2 = int(individuo2, 2)
    x1 = Data.limite_inferior + numero_decimal1*Data.resolucion
    x2 = Data.limite_inferior + numero_decimal2*Data.resolucion
    y1 = calcular_funcion(funcion, x1)
    y2 = calcular_funcion(funcion, x2)
    
    individuo1 = Individuo(i=numero_decimal1, binario=individuo1, x=x1, y= y1)
    
    
    individuo2 = Individuo(i=numero_decimal2, binario=individuo2, x=x2, y= y2)
    Data.poblacion_general.append(individuo1)
    Data.poblacion_general.append(individuo2)
    
    
    #flag = True
    #if Data.tipo_problema_value == "Minimizacion":
    #    flag = False
    #individuos_ordenados = sorted(Data.poblacion_general, key=lambda x: x.y, reverse=flag)
    
    
    #("Toda la poblacion es:")
    #for individuo in individuos_ordenados:
    #print(individuo)