# returns all characters that an iterable and a list have in common
# I think that for small scales, iterating over a list is faster than iterating over a string
def in_common(mex,symbols): 
    common = []
    for i in range(len(symbols)):
        if symbols[i] in mex and symbols[i] not in common:
            common.append(symbols[i])
    return common


# test change 2
