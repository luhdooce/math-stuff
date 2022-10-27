def in_common(mex,symbols):
    common = []
    for i in range(len(symbols)):
        if symbols[i] in mex and symbols[i] not in common:
            common.append(symbols[i])
    return common

    