def calcScore(t, w):
    return (t + (-t/w)) * 100

def getScore(bm_time):
    final = []
    # Pesos
    # Escrever arquivos -> 10
    # Processar dados   -> 7
    # Ler arquivos/RAM  -> 3

    final.append(calcScore(bm_time[0], 3))
    final.append(calcScore(bm_time[1], 7))
    final.append(calcScore(bm_time[2], 10))
    final.append(sum(final))

    return final