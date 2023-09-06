# imports

# data

X = [1, 2, 3, 4, 5, 6]
Y = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]

# formula 3, 4
def border_one_dif(y1, y2, h):
    return (y2 - y1) / h
# formula 5
def center_one_dif(y0, y2, h):
    return (y2 - y0) /(2 * h)

# formula 6
def two_dif(y0, y1, y2, h):
    return (y0 - 2*y1 + y2) / h / h

def make_one_dif(x, y):
    ans = []
    for i in range(len(x) - 1):
        ans.append(border_one_dif(y[i], y[i + 1], x[i + 1] - x[i]))
    ans.append(0)
    return ans

def make_center_dif(x, y):
    ans = [0]
    for i in range(len(x) - 2):
        ans.append(center_one_dif(y[i], y[i + 2], x[i + 1] - x[i]))
    ans.append(0)
    return ans

def make_two_dif(x, y):
    ans = [0]
    for i in range(len(x) - 2):
        ans.append(two_dif(y[i], y[i + 1], y[i + 2], x[i + 1] - x[i]))
    ans.append(0)
    return ans

def Runge2(h, y1, y2, y3):
    m = 2
    p = 3
    ih = border_one_dif(y1, y2, h)
    imh = border_one_dif(y1, y3, m*h)
    i = ih + (ih - imh) / (m**p - 1)
    return i

def make_2runge(x, y):
    ans = [0]
    for i in range(len(x) - 2):
        ans.append(Runge2(y[i], y[i + 1], y[i + 2], x[i + 1] - x[i]))
    ans.append(0)
    return ans

def print_table(x, y, od, cd, td, sv, r2d):
    print("{:3}{:^10}{:^10}{:^10}{:^10}{:^10}{:^10}".format("x", "y", 1, 2, 3, 4, 5))
    for i in range(len(x)):
        print("{:^3}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}{:10.4f}".format(x[i], y[i], od[i], cd[i], r2d[i], sv[i], td[i]))

def make_spec_variables(x, y):
    eta = []
    xi = []
    for i in range(len(x)):
        eta.append(1/x[i]) 
        xi.append(1/y[i])
    return eta, xi

def make_y_from_eta_xi(xieta, xiy, etax):
    ans = []
    for i in range(len(xieta) - 1):
        res = xieta[i] * etax[i] / xiy[i]
        ans.append(res)
    ans.append(0)
    return ans

def make_spec_var_diff(x, y):
    eta, xi = make_spec_variables(x, y)

    xieta = make_one_dif(eta, xi)
    xiy = make_one_dif(y, eta)
    etax = make_one_dif(x, xi)

    ans = make_y_from_eta_xi(xieta, xiy, etax)
    return ans

if __name__ == '__main__':
    one_dif = make_one_dif(X, Y)
    center_diff = make_center_dif(X, Y)
    two_diff = make_two_dif(X, Y)
    spec_var = make_spec_var_diff(X, Y)
    runge2 = make_2runge(X, Y)
    print_table(X, Y, one_dif, center_diff, two_diff, spec_var, runge2)

