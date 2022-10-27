from recursivefunctions import factorial
import math
def func_parse(function,x):
    func_names = {
        'sin' : math.sin(x), 
        'cos' : math.cos(x), 
        'tan' : math.tan(x), 
        'fact' : factorial(x)
        }
    for i in func_names:
        if function == i:
            return func_names[function]
        
print(func_parse('sin',5))