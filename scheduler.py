from concurrent.futures import ThreadPoolExecutor

#wykonanie danej operacji
def execute_operation(op, matrix,results):
    if op[0] == 'A':
        i, k = op[1]-1, op[2]-1

        results[('A',i,k)] =  matrix[k][i] / matrix[i][i]

    elif op[0] == 'B':
        i, j, k = op[1]-1, op[2]-1, op[3]-1
        m_k_i = results[('A',i,k)]

        results[('B',i,j,k)] = matrix[i][j] * m_k_i

    elif op[0] == 'C':
        i, j, k = op[1]-1, op[2]-1, op[3]-1
        n_k_i = results[('B',i,j,k)]

        matrix[k][j] -= n_k_i
    else:
        raise ValueError("Nieznana operacja")
    return


#wykonanie alg. eliminacji gaussa po uwzglednieniu klas Foaty
#wszystkie operacje w danej klasie możeny wykonać równolegle 
def scheduler(fnf, matrix):

    results = {}

    for layer in fnf:
        #zarzadzanie pula watkow
        with ThreadPoolExecutor() as executor:
            #executor.submit - odpala w nowym watku
            futures = [executor.submit(execute_operation, op, matrix,results) for op in layer]

            #synchronizacja
            for future in futures:
                future.result() 
    return matrix