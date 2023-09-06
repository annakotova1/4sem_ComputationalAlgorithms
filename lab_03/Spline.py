
def make_table_y_x2(x_start, x_end, h):
    table = []
    cur_x = x_start
    while cur_x <= x_end:
        table.append([cur_x, cur_x**2])
        cur_x+=h
    return table

def copy_table(table):
    new_table = []
    for i in range(len(table)):
        new_pair = []
        for j in range(len(table[i])):
            new_pair.append(table[i][j])
        new_table.append(new_pair)
    return new_table

def translate_table_to_array(table):
    x_array = []
    y_array = []
    for i in range(len(table)):
        x_array.append(table[i][0])
        y_array.append(table[i][1])
    return x_array, y_array

def output_array(array):
    for i in range(len(array)):
        print(array[i], end=" ")
    print()

def output_table(table):
    print("|{:4}|{:4}|".format("X", "Y"))
    for i in range(len(table)):
        print("|{:4}|{:4}|".format(table[i][0], table[i][1]))

# NEWTHON

def copy_array(arr):
    new_arr = []
    for x in arr:
        new_arr.append(x)
    return new_arr

def newtonian_step_of_differences(x_array, y_array):
    next_y_array = []
    x_step = len(x_array) - len(y_array) + 1
    
    for i in range(len(y_array) - 1):
        difference = (y_array[i] - y_array[i+1])/(x_array[i] - x_array[i+x_step])
        next_y_array.append(difference)
    return next_y_array

def newtonian_find_coef(x_array, y_array, n):
    coefs = [y_array[0]]
    cur_n = 0
    while len(y_array)!= 1:
        y_array = newtonian_step_of_differences(x_array, y_array)
        coefs.append(y_array[0])
        cur_n += 1
        if (cur_n >= n):
            break
    return coefs

def newtonian_solve_polinom(x_array, y_array, x, n):
    coefs = newtonian_find_coef(x_array, y_array, n)
    res = coefs[0]
    mnoj = 1
    for i in range(1, len(coefs)):
        mnoj *= (x - x_array[i - 1]) 
        res += coefs[i] * mnoj
    return res


# SPLINE
def get_h(table, N):
    h = [0, table[1][0] - table[0][0]] 
    for i in range(2,N+1):
        h.append(table[i][0]-table[i-1][0])
    return h

def get_kci_etta(table, N, h):
    kci = [0, 0, 0]
    etta = [0, 0, 0]
    for i in range(2,N+1):
        f = 3 * ((table[i][1] - table[i-1][1]) / h[i] - (table[i-1][1] - table[i-2][1]) / h[i-1])
        kci.append(-h[i]/(h[i-1]*kci[i]+2*(h[i-1]+h[i])))
        etta.append((f-h[i-1]*etta[i])/(h[i-1]*kci[i]+2*(h[i-1]+h[i])))
    return kci, etta

def get_c(table, N, kci, etta):
    c = [0,0]
    for i in range(N-1,0,-1):
        c.insert(0, kci[i+1] * c[0] + etta[i+1])
        c.insert(0,0)
    return c

def get_abd(table, N, h, c):
    a=[0]
    b=[0]
    d=[0]
    for i in range(1,N+1):
        a.append(table[i-1][1])
        b.append((table[i][1]-table[i-1][1])/h[i]-h[i]*(c[i+1]+2*c[i])/3)
        d.append((c[i+1]-c[i])/(3*h[i]))
    return a, b, d

def get_pos(table, N, x):
    for i in range(N):
        if table[i][0]<=x and table[i+1][0]>x:
            pos=i+1
            break
    return pos

def calculate_answer(table, x, a, b, c, d, pos):
    return (a[pos]+b[pos]*(x-table[pos-1][0])+c[pos]*(x-table[pos-1][0])**2+d[pos]*(x-table[pos-1][0])**3)

def spline(table, x):
    N = len(table) - 1
    h = get_h(table, N)
    kci, etta = get_kci_etta(table, N, h)
    c = get_c(table, N, kci, etta)
    a, b, d = get_abd(table, N, h, c)
    pos = get_pos(table, N, x)
    return calculate_answer(table, x, a, b, c, d, pos)

def main():
    main_table = make_table_y_x2(0, 10, 1)

    x1 = 0.5
    x2 = 5.5

    print("Дана таблица:")
    output_table(main_table)
    print("х1:")
    print("\tТочное значение: ", x1**2)
    print("\tРезультат интерполяции кубическим сплайном: ", spline(main_table,x1))
    x_array, y_array = translate_table_to_array(main_table)
    print("\tРезультат интерполяции полиномом Ньютона 3-ей степени: ", newtonian_solve_polinom(x_array, y_array, x1, 3))
    print("х2:")
    print("\tТочное значение: ", x2**2)
    print("\tРезультат интерполяции кубическим сплайном: ", spline(main_table,x2))
    x_array, y_array = translate_table_to_array(main_table)
    print("\tРезультат интерполяции полиномом Ньютона 3-ей степени: ", newtonian_solve_polinom(x_array, y_array, x2, 3))

main()