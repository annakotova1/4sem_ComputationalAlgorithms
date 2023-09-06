def make_matrix(t, ans):
    matrix = []
    cur_arr = []
    for i in range(len(ans)):
        cur_arr = []
        for j in range(len(t)):
            #print(j, pow(t[j], i))
            cur_arr.append(pow(t[j], i))
        cur_arr.append(ans[i])
        matrix.append(cur_arr)
    return matrix 

def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            print(round(matrix[i][j], 4), end="  ")
        print()
    print()


def solve_matrix(matrix):
    #print_matrix(matrix)
    for i in range(len(matrix)):
        #print(i)
        coef = matrix[i][i]
        arr = []
        for j in range(i, len(matrix[i])):
            matrix[i][j] = matrix[i][j]/coef
            arr.append(matrix[i][j])
        for j in range(i + 1, len(matrix)):
            new_coef = matrix[j][i]
            for k in range(i, len(matrix[i])):
                matrix[j][k] = matrix[j][k] - arr[k - i] * new_coef
        #print_matrix(matrix)

    for i in range(len(matrix) - 1, 0, -1):
        #print(i)
        coef = matrix[i][i]
        arr = []
        for j in range(i, len(matrix[i])):
            matrix[i][j] = matrix[i][j]/coef
            arr.append(matrix[i][j])
        for j in range(i - 1, -1, -1):
            new_coef = matrix[j][i]
            for k in range(i, len(matrix[i])):
                matrix[j][k] = matrix[j][k] - arr[k - i] * new_coef
        #print_matrix(matrix)

    ans = []
    for i in range(len(matrix)):
        ans.append(matrix[i][len(matrix[i]) - 1])
    return ans

