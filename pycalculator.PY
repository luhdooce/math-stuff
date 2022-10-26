def main():
    expression = '4+(5+(6)^2+8*9^(8))+5*2'
    print(deparenthesize(numerize(expression)))
    
def deparenthesize(mex: list) -> list:
    c = 0
    left = 0
    while ('(' in mex or ')' in mex) and c < len(mex):
        if mex[c] == '(':
            left = c
            c += 1
        elif mex[c] == ')':
            #print(mex[left],mex[left+1:c],mex[c])
            mex[left] = solve(mex[left+1:c])
            mex = mex[:left+1]+mex[c+1:]
            c = 0 # need to restart from the beginning, in case we missed some opening parentheses along the way (almost guaranteed, since we evaluate from innermost parentheses outwards)
            
            #print('mex becomes ', mex)
        else:
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
        
def solve(mex: list):
    if len(mex) == 1:
        return mex[0]
    c = 0
    while '^' in mex and c < len(mex):
        if mex[c] == '^':
            mex[c-1] = str(pow(float(mex[c-1]),float(mex[c+1])))
            mex = mex[:c]+mex[c+2:]
        else:
            c += 1
            
    c = 0
    while ('*' in mex or '/' in mex) and c < len(mex):
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
    while ('+' in mex or '-' in mex) and c < len(mex):
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

def calculate(mex):
    return float(deparenthesize(numerize(mex)))

main()