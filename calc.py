from sympy import symbols, lambdify

def calcular_funcion(*args):
    x = symbols('x')
    expresion = lambdify(x, funcion.replace('sen', 'sin'), 'numpy')
    resultado = expresion(x_valor)
    return resultado

funcion = "x**4 - 2*x**2 + cos(x)"
x_valor = 6  # Puedes cambiar esto según tu necesidad

resultado = calcular_funcion(funcion, x_valor)
print(f"El resultado de evaluar la función en x={x_valor} es: {resultado}")



