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
    
    funcion = "(x**3 * sin(x))/100 + x**2 *cos(x)"
    
    poblacion_inicial = int(data.p_inicial)
    poblacion_maxima = float(data.p_max)
    resolucion = float(data.res)
    limite_inferior = float(data.lim_inf)
    limite_superior = float(data.lim_sup)
    prob_mutacion_ind = float(data.prob_ind)
    prob_mutacion_gen = float(data.prob_gen)
    
    #Empezamos sacando los datos 
    rango = limite_superior - limite_inferior
    num_saltos = rango/resolucion
    num_puntos = num_saltos + 1
    num_bits = int(math.log2(num_puntos) + 1)
    
    rango_numero= 2**num_bits #256
    

    individuos = []
    for i in range(poblacion_inicial):
        num_generado = (random.randint(0, rango_numero))
        num_generado_binario = (bin(num_generado)[2:])
        valor_x = limite_inferior + num_generado*resolucion
        valor_y = calcular_funcion(funcion, valor_x)
        
        individuo = Individuo(id=i+1, i=num_generado, binario=num_generado_binario, x=valor_x, y= valor_y)
        individuos.append(individuo)
    
    
    
    for individuo in individuos:
        print(f"ID: {individuo.id}, Binario: {individuo.binario}, i: {individuo.i}, x: {individuo.x}")
