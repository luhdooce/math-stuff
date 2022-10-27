# test git push change

def main():
    P = '4+(5+(6)^2+8*9^(8))+5*2'
    print(calculate(P))
    
def deparenthesize(mex: list) -> list:
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
    c = 1
    
    while c < len(mex): 
        if mex[c].isnumeric(): # check if current symbol is a digit
            if mex[c-1].isnumeric(): # check if previous element contains only digits
                # add current symbol to the previous element (appending onto the previous number)
                hold = mex[c]
                mex.pop(c)
                mex[c-1] += hold
            else: # if not, then we just move on
                c += 1
        else: # if current symbol is not a digit, move on
            c += 1
            
    return mex 
        
'''
All operations use the a?b format where ? is some operator (e.g. a^b, a+b, a/b, etc.). we replace 'a' with the result 
of the operation, and get rid of the operator and b (i.e. slice out '?b'). 

Notice that we don't increment the iterator 'c' if we complete an 'a?b' operation. Since we are slicing out part of 
the string, we want to avoid the "shifting window" problem

'''
def solve(mex: list):
    if len(mex) == 1:
        return mex[0]
    c = 0
    while '^' in mex and c < len(mex): # if we find exponent sign
        if mex[c] == '^':
            mex[c-1] = str(pow(float(mex[c-1]),float(mex[c+1]))) 
            mex = mex[:c]+mex[c+2:]
        else:
            c += 1
            
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
    while ('+' in mex or '-' in mex) and c < len(mex): # if we find addition or subtraction sign
        if mex[c] == '+':
            # print(mex[c-1],mex[c],mex[c+1])
            mex[c-1] = str(float(mex[c-1])+float(mex[c+1]))
            mex = mex[:c]+mex[c+2:]
        elif mex[c] == '-':
            #print(mex[c-1],mex[c],mex[c+1])
            mex[c-1] = str(float(mex[c-1])-float(mex[c+1]))
            mex = mex[:c]+mex[c+2:]
        else:
            c += 1
            
    return str(mex[0])

def calculate(mex): # combines the other functions 
    return float(deparenthesize(numerize(mex)))

main()