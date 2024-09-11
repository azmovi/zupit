def valor(vetor):
    if vetor[0] != 0:
        return 0

    total = sum(vetor)
    total_esperado = (vetor[0] + len(vetor)) * (len(vetor) + 1) // 2

    return total_esperado - total


print(valor([0, 1, 2, 3, 4, 5, 6, 7, 9, 10]))
