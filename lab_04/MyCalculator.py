import numpy as np
import matplotlib.pyplot as plt

def f(x_arr, coeff):    
    res = np.zeros(len(x_arr))
    for i in range(len(coeff)):        
        res += coeff[i]*(x_arr**i)
    return res                   

def get_lyne_style(i):
    return ["solid", "dotted", "dashed", "--", ':', "-."][i %6]

def my_solve(A, B):    
    n =len(B)
    for col_i in range(n):
        for row_i in range(col_i+1, n):            
            coeff =-(A[row_i][col_i] / A[col_i][col_i])
            for j in range(col_i, n):                
                A[row_i][j] += coeff*A[col_i][j]            
            B[row_i] += coeff*B[col_i]    
    
    x = [0] * n
    for i in range(n-1, -1, -1):
        for j in range(n-1, i, -1):            
            B[i] -= x[j]*A[i][j]        
        x[i] = B[i]/A[i][i]
    return x
# n - Степень полинома
def get_coeff(ro, x_s, y_s, n, N):
    #if n >= N or n < 0:
    #    raise ArithmeticError("Невозможно составить полином данной степени")    
    n +=1    
    A = [[0] * n] * n    
    B = [0] * n
    for k in range(n):        
        A[k] = [sum([ro[i] * (x_s[i]**(k + m)) for i in range(N)]) for m in range(n)]        
        B[k] =sum([ro[i] * y_s[i] * (x_s[i]**k) for i in range(N)])
    return my_solve(A, B)
    #return np.linalg.solve(A, B)

def print_plot(min_x, max_x, n, a_s, j, color):
    for i in range(n-1, -1, -1):        
        x_for_plot = np.arange(min_x, max_x, 0.01)        
        print(a_s[j][i])
        plt.plot(x_for_plot, f(x_for_plot, a_s[j][i]), 'k', linestyle=get_lyne_style(i), color=color)    


def print_answer(x, y, ro, a_s):    
    n = len(a_s[0])    
    min_x, max_x =min(x), max(x)    
    plt.grid(True)
    print_plot(min_x, max_x, n, a_s, 0, "blue")
    print_plot(min_x, max_x, n, a_s, 1, "green")
    plt.legend()
    for j in range(len(x)):
        plt.plot(x[j], y[j], 'ro', markersize=ro[j]+3)    
    
    plt.show()

def make_arrays(table):
    x = []
    y = []
    ro = []
    for i in range(len(table)):
        x.append(table[i][0])
        y.append(table[i][1])
        ro.append(table[i][2])
    return x, y, ro

class MyCalculator:
    def drawPlot(self, myTable, n_end = 3):
        x, y, ro = make_arrays(myTable)
        
        n_start = 1
        coeffs = []
        try:
            x_len = len(x)
            ro_len = len(ro)
            # Получаем коэффициенты для разных n
            coeffs.append([get_coeff(ro, x, y, n, x_len) for n in range(n_start, n_end+1)]) 
            coeffs.append([get_coeff([1 for _ in range(ro_len)], x, y, n, x_len) for n in range(n_start, n_end+1)])
        except ArithmeticError as err:
            print("ArithmeticError")
            return
        except:
            print("error")
            return

        print_answer(x, y, ro, coeffs)
