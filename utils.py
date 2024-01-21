def output(pairs, colon=1):
    for k in list(pairs.keys()):
        print(str(k) + ':'*(colon==1), str(pairs[k]))