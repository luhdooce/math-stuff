from basic_check_functions import in_common
from recursivefunctions import factorial
import math
    
    
# functions use the fx format. First, the user inputs in the form of f(x). The program then
# removes the parentheses to make it a format of fx (as two elements), and then immediately 
# attempts to solve fx and simplify it to a single element. It replaces 'f' with this element
# and removes 'x' from the list
def desymbolize(mex: list) -> list: # aims to simplify symbols like parentheses or functions
    
    c = 0
    left = 0
    
    while ('(' in mex or ')' in mex) and c < len(mex): # check if parentheses in math expression
        if mex[c] == '(': # track latest OPEN parenthesis
            left = c
            c += 1 # keep moving
        elif mex[c] == ')': # check for CLOSING parenthesis
            #print(mex[left],mex[left+1:c],mex[c])
            '''
            solve the part between the parentheses, use it to replace the opening parenthesis, and 
            get rid of the remaining expression between the parentheses and the CLOSING parenthesis 
            '''
            mex[left] = solve(mex[left+1:c]) 
            mex = mex[:left+1]+mex[c+1:] # 
            
            # check if something precedes our newly formed value, 
            # and if it's a function
            if 0 <= left-1 and mex[left-1].isalpha(): 
                # pass in the name of the previous function, and the input into the function
                mex[left-1] = func_parse(mex[left-1],mex[left]) 
                mex.pop(left) # remove the remaining value (see guide above this code function)
                # mex = mex[:left]+mex[left+1:] also works instead of pop()
                
            c = 0 # need to restart from the beginning, in case we missed some opening parentheses along the way (almost guaranteed, since we evaluate from innermost parentheses outwards)
            #print('mex becomes ', mex)
        else: 
            # keep going
            c += 1
    return solve(mex)
        
def numerize(mex: str) -> list: # converts the string expression into a parsed list
    if len(mex) == 1:
        return mex[0]
    # suppose string = '345+879'
    mex = list(mex)
    c = 0
    ops,parenths = ['*','-','+','/','^'],['(',')']
    num_digs = ['.','0','1','2','3','4','5','6','7','8','9']
    while c < len(mex): 
        # in_common checks how many 
        if len(in_common(mex[c],num_digs)) > 0: # check if current symbol is a digit or a decimal point
            # check if previous element contains only digits or decimal points
            # also must ensure that there actually IS a previous element
            if 0 < c and len(in_common(mex[c-1],num_digs)) > 0: 
                # add current symbol to the previous element (appending onto the previous number)
                hold = mex[c]
                mex.pop(c)
                mex[c-1] += hold
            else: # if not, then we just move on
                c += 1
        elif mex[c].isalpha(): # check if current symbol is a letter
            if mex[c-1].isalpha():
                hold = mex[c]
                mex.pop(c)
                mex[c-1] += hold
            else:
                c += 1
        
        elif mex[c] == '-': # check if there is a negative sign
            print('ass')
            if 0 <= c-1: # check if there is a previous symbol
                # check if previous symbol is a number or the end of a parenthesis block
                if mex[c-1].isnumeric or mex[c-1] == ')': 
                    mex[c] = '+'
                
            # replace '-' with '+(-1)*' (so we're multiplying by -1). This time, the 
            # '-1' is an element on its own
            mex.insert(c+1, '(') 
            mex.insert(c+2, '-1')
            mex.insert(c+3, ')')
            mex.insert(c+4, '*')
            '''
            elif 0 <= c-1 and mex[c-1] in symbs:
                mex[c+1] = '-' + mex[c+1]
                mex.pop(c)
                c -= 1
            elif c == 0:
                mex[c+1] = '-' + mex[c+1]
                mex.pop(c)
            '''
        else: # if current symbol is not a digit, move on
            c += 1
    
    return mex 
        

# All operations use the a?b format where ? is some operator (e.g. a^b, a+b, a/b, etc.). we replace 'a' with the result 
# of the operation, and get rid of the operator and b (i.e. slice out '?b'). 
# Notice that we don't increment the iterator 'c' if we complete an 'a?b' operation. Since we are slicing out part of 
# the string, we want to avoid the "shifting window" problem


def solve(mex: list):
    if len(mex) == 1:
        return mex[0]
    
    c = len(mex)-1
    while '^' in mex and c > -1: # if we find exponent sign
        if mex[c] == '^':
            mex[c-1] = str(pow(float(mex[c-1]),float(mex[c+1]))) 
            mex = mex[:c]+mex[c+2:]
            c -= 2 
            '''
            since we're slicing out some of the string, and since 'c' approaches from the upper end of the 
            string, then we need to shift c over by how many elements are getting deleted (which is 2, if we 
            consider the a?b system)
            '''
        else:
            c -= 1
    '''
    We do this in reverse, because if we have something like 2^2^3, we want to evaluate it in reverse (i.e. evaluate
    using the order of 2^(2^3))
    '''
            
    c = 0
    while ('*' in mex or '/' in mex) and c < len(mex): # if we find multiplication or division sign
        if mex[c] == '*':
            # print(mex[c-1],mex[c],mex[c+1])
            
            mex[c-1] = str(float(mex[c-1])*float(mex[c+1]))
            mex = mex[:c]+mex[c+2:]
        elif mex[c] == '/':
            # print(mex[c-1],mex[c],mex[c+1])
            mex[c-1] = str(float(mex[c-1])/float(mex[c+1]))
            mex = mex[:c]+mex[c+2:]
        else:
            c += 1
            
    c = 0
    while c < len(mex): 
        if mex[c] == '+':
            # print(mex[c-1],mex[c],mex[c+1])
            mex[c-1] = str(float(mex[c-1])+float(mex[c+1]))
            mex = mex[:c]+mex[c+2:]
        # elif mex[c][0] == '-':
            # print(mex[c-1],mex[c],mex[c+1])
            # print(mex[c])
            # mex[c-1] = str(float(mex[c-1])+float(mex[c]))
            # mex = mex[:c]+mex[c+1:]
        else:
            c += 1
            
    return str(mex[0])

def func_parse(function,x): 
    x = float(x)
    func_names = {
        'sin' : math.sin(x), 
        'cos' : math.cos(x), 
        'tan' : math.tan(x), 
        'fact' : factorial(x),
        'sqrt' : math.pow(x,1/2)
        }
    for i in func_names:
        if function == i:
            return func_names[function]
    # add a check here, in case the function is not defined

def calculate(mex): # combines the other functions 
    return desymbolize(numerize(mex))