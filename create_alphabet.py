#zapisywanie macierzy wynikowej do pliku
def save_matrix_to_file(file_path,matrix):
    try:
        with open(file_path,'w') as file:
            file.write(f"{len(matrix)}\n")

            for row in matrix:
                file.write(" ".join(map(str, row[:-1])) + "\n")

            x_vector = [round(row[-1],10) for row in matrix]
            file.write(" ".join(map(str, x_vector)) + "\n")
            
    except Exception as e:
        print(f"Error while saving to file: {e}")
    return

#tworzenie macierzy z pliku
def create_matrix_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            
        num_rows = int(lines[0].strip())

        matrix = []
        x_vector = list(map(float, lines[-1].strip().split()))
        i = 0
        for line in lines[1:-1]:
            row = list(map(float, line.strip().split()))
            row.append(x_vector[i])
            i += 1

            matrix.append(row)

        return matrix

    except Exception as e:
        print(f"Error while reading from file: {e}")
        return []

def m_idx(i):
    return i + 1

#jedna iteracja w algorytmie gauss'a - czyli wyzerowanie elementu M(i,k)
#zgodnie z naszą teorią to ciąg operacji s(i,k)
#tworzymy alfabet sigma
def gauss_iteration(M,i,k,sigma):
    cols = len(M[0])

    #operacja A
    # m_k_i = M[k][i] / M[i][i]
    sigma.append(('A', m_idx(i), m_idx(k)))

    for j in range(i,cols):
        #operacja B
        # n_k_i = M[i][j] * m_k_i
        sigma.append(('B', m_idx(i), m_idx(j), m_idx(k)))

        #operacja C
        # M[k][j] -= n_k_i
        sigma.append(('C', m_idx(i), m_idx(j), m_idx(k)))
        
    return

#cały gauss czyli ciąg wszystkich podciągów s(i,k)
def create_sigma(M):
    rows = len(M)

    sigma = []

    for i in range(rows-1):
        for k in range(i+1,rows):
            gauss_iteration(M,i,k,sigma)

    return sigma
    
    
