from math import sin, cos, exp, pi 
from scipy.optimize import bisect
import numpy
import time
from Matrix import make_matrix,solve_matrix
import matplotlib.pyplot as plt
EPS = 1e-6
N = 10

# 3
def legandra(t):
    temp1 = 1
    temp2 = t
    
    for i in range(2, N + 1):
        cur = 1 / i * ((2 * i - 1) * t * temp2 - (i - 1) * temp1)
        temp2, temp1 = cur, temp2
    return cur

def dichotomy_method(a, b):
    return bisect(legandra, a, b, xtol = EPS)
def legandra_roots(n):
    # ищем отрезки с корнями
    h = 1 / 2 / n
    #print(n)
    global N 
    N = n
    count_root = 0
    while (count_root != n):
        #print(count_root, n)
        cur = -1
        count_root = 0
        SEGMENT = []
        while (cur < 1):
            
            if legandra(cur) * legandra(cur + h) < 0:
                SEGMENT.append([cur, cur + h])
                count_root += 1
                #print(count_root, cur, cur+h, legandra(cur), legandra(cur + h))
            cur += h
        h /= 2

    # ищем корни
    #print("\n", SEGMENT, "\n")
    ROOT = []
    for seg in SEGMENT:
        ROOT.append(dichotomy_method(seg[0], seg[1]))

    return ROOT     
    

# Ответы на систему уравнений 5.2(?) из лекций

def get_roots(n):
    arr = []
    for i in range(n):
        if (i%2 == 0):
            arr.append(2 / (i+1))
        else:
            arr.append(0)
    return arr

def test1():
    matrix = [[1, 1, -2],
              [1, -1, 1]] 
    ans = solve_matrix(matrix)
    for i in range(len(ans)):
        print(round(ans[i], 4))
    print(ans)

def l_R(omega, fita):
    a =  2 * cos(omega)/(1 - (sin(omega)**2) * (cos(fita)**2))
    return a
def f1(tao, omega, fita):
    a = (1 - exp(-tao*(l_R(omega, fita)))) * cos(omega) * sin(omega)
    return a

def integrate_gayss(a, b, t, a_coef, tao, fita):
    res = 0
    for i in range(len(a_coef)):
        res += (b-a)/2*a_coef[i] * f1(tao, (a + b)/2 + (b - a)/2*t[i], fita) #(b-a)/2*
    #print(res, a, b, tao, fita)
    return res


def find():
    n = 5
    t = legandra_roots(n)
    ans = get_roots(n)
    matrix = make_matrix(t, ans)
    print()
    print(t)
    print()
    print(ans)
    print()
    print(len(t), len(ans), len(matrix), len(matrix[0]))
    for i in range(len(matrix)):
        print(matrix[i])

    res = solve_matrix(matrix)
    print(res)
    print()


# Simpson
def f2(a, b, tao, fita, n):
    t = legandra_roots(n)
    ans = get_roots(n)
    matrix = make_matrix(t, ans)
    a_coef = solve_matrix(matrix)
    return integrate_gayss(a, b, t, a_coef, tao, fita)

def get_simpson_parts(a, b, n):
    parts = []
    h = (b - a)/(2* n - 1)
    cur = a
    for i in range(2*n - 1):
        parts.append([cur, cur+h])
        cur += h
    return parts

def integrate_simpson(a1, b1, a2, b2, tao, n1):
    result = 0

    fita = a2
    result += f2(a1, b1, tao, fita, n1)
    #print(result)
    fita = (a2 + b2)/2
    result += 4 * f2(a1, b1, tao, fita, n1)
    #print(result)
    fita = b2
    result += f2(a1, b1, tao, fita, n1)
    #print(result)

    result *= (b2-a2)/6
    #print(result)
    return result

def big_integrate_simpson(a1, b1, a2, b2, tao, n1, n2):
    parts = get_simpson_parts(a2, b2, n2)
    #print(parts)
    result = 0
    for cur_part in parts:
        result += integrate_simpson(a1, b1, cur_part[0], cur_part[1], tao, n1)
    return result

def epsilon(tao, n1, n2):
    return 4/pi *big_integrate_simpson(0, pi/2, 0, pi/2, tao, n1, n2)

def test():
    x = symbols("x")
    print(legrange(x, 1))
    print(legrange(x, 2))
    print(legrange(x, 3))
    print(legrange(x, 4))

    print()
    print(legrange(x, 2))
    s = lambdify(x, legrange(x, 2))
    print(s(4))

    print()
    print(legrange(x, 10))
    s = lambdify(x, legrange(x, 10))
    print(s(1))

    print(legandra_roots(10))


def draw_plot(n):
    q = []
    ans = []
    for i in range(200):
        #print(i/20)
        q.append(i/20)
        ans.append(epsilon(i/20, n,n))
    plt.plot(q, ans)
    plt.ylabel('N = {}'.format(n))
    plt.show()

if __name__ == '__main__':
    tao = float(input("Введите tao: "))
    n2 = int(input("Введите NSimpson: "))
    n1 = int(input("Введите NGayss: "))
    print("Результат интеграла: ", round(epsilon(tao, n1, n2), 6)) 
    print(legandra_roots(1))


    n = int(input("Введите N для графика: "))

    draw_plot(n)
