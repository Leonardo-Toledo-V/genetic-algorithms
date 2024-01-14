import math
import random
from sympy import symbols, lambdify

class Individuo:
    def __init__(self, id, binario, i, x, y):
        self.id = id
        self.binario = binario
        self.i = i
        self.x = round(x, 4)
        self.y = round(y, 4)

def calcular_funcion(funcion, valor_x):
    x = symbols('x')
    expresion = lambdify(x, funcion, 'numpy')
    resultado = expresion(valor_x)
    return resultado

def genetic_algorithm(data):
        
    poblacion_inicial = int(data.p_inicial)
    poblacion_maxima = int(data.p_max)
    resolucion = float(data.res)
    limite_inferior = float(data.lim_inf)
    limite_superior = float(data.lim_sup)
    prob_mutacion_ind = float(data.prob_ind)
    prob_mutacion_gen = float(data.prob_gen)
    tipo_problema_value = data.tipo_problema
    
    #Empezamos sacando los datos 
    rango = limite_superior - limite_inferior
    num_saltos = rango/resolucion
    num_puntos = num_saltos + 1
    num_bits = int(math.log2(num_puntos) + 1)
    rango_numero= 2**num_bits #256
    num_bits_necesarios = len(bin(rango_numero)[2:])
    
    inicializacion(poblacion_inicial, rango_numero, limite_inferior, resolucion, num_bits_necesarios, tipo_problema_value);


def inicializacion(poblacion_inicial, rango_numero, limite_inferior, resolucion, num_bits_necesarios, tipo_problema_value):
    funcion = "(x**3 * sin(x))/100 + x**2 *cos(x)"
    individuos = []
    for i in range(poblacion_inicial):
        num_generado = (random.randint(0, rango_numero))
        num_generado_binario = (bin(num_generado)[2:]).zfill(num_bits_necesarios)
        valor_x = limite_inferior + num_generado*resolucion
        valor_y = calcular_funcion(funcion, valor_x)
        individuo = Individuo(id=i+1, i=num_generado, binario=num_generado_binario, x=valor_x, y= valor_y)
        individuos.append(individuo)
    
    optimizacion(individuos, tipo_problema_value)


def optimizacion(individuos, tipo_problema_value):
    #Estrategia A3: (100 %) la población se ordena y particiona en dos, los individuos de la
    #partición con mejor aptitud se cruzan con algunos o todos los individuos.
    flag = True
    if tipo_problema_value == "Minimizacion":
        flag = False
        mejor_individuo = min(individuos, key=lambda x: x.y)
    else:
        flag = True
        mejor_individuo = max(individuos, key=lambda x: x.y)
    # Se ordenan todos los individuos para posteriormente particionarlos
    individuos_ordenados = sorted(individuos, key=lambda x: x.y, reverse=flag)
    
    #Particionamos en dos elementos y separamos la mejor aptitud, y los de peor aptitud
    mitad = int(len(individuos_ordenados) / 2)
    particion_mejor_aptitud = individuos_ordenados[:mitad]
    otra_parte_poblacion = individuos_ordenados[mitad:]

    for individuo in individuos_ordenados:
        print(f"ID: {individuo.id}, i: {individuo.i}, Binario: {individuo.binario}, X: {individuo.x}, Y: {individuo.y}")

    mejor_valor_y = mejor_individuo.y
    print(f"ID: {mejor_individuo.id}, Mejor Y: {mejor_valor_y}")
    print("Poblacion con mejor aptitud", [individuo.id for individuo in particion_mejor_aptitud])
    print("Resto de poblacion", [individuo.id for individuo in otra_parte_poblacion])
        






def emparejamiento():
    print("hello")

def cruza():
    print("hello")

def mutacion():
    print("hello")

def poda():
    print("hello")

