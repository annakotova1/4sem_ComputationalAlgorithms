from math import fabs

EPS = 0.00001

MAX_N = 4

def read_file(filename):
	file = open(filename, 'r')
	x_array = []
	y_array = []
	y1_array = []
	for line in file:
		line_array = line.split()
		x_array.append(float(line_array[0]))
		y_array.append(float(line_array[1]))
		y1_array.append(float(line_array[2]))
	return x_array, y_array, y1_array

def sort_start_data(x_array, y_array, y1_array):
	for k in range(len(x_array)-1):
		for i in range(len(x_array)-1):
			if (x_array[i] > x_array[i+1]):
				x_array[i], x_array[i+1] = x_array[i+1], x_array[i]
				y_array[i], y_array[i+1] = y_array[i+1], y_array[i]
				y1_array[i], y1_array[i+1] = y1_array[i+1], y1_array[i]

def get_index_to_work_table(x_array, x):
	index = 0
	for i in range(len(x_array)):
		if x < x_array[i]:
			index = i
			break
	return index

def make_one_work_array(array, index, n):
	if (index - (n + 1) / 2) < 0:
		new_array = array[0:n + 1]
	elif ((n + 1) / 2 + index) > len(array):
		new_array = array[len(array) - 1 - n:]
	else:
		new_array = array[index - ((n + 1) // 2): index - ((n + 1) // 2) + n + 1]
	return new_array

def make_work_tables(x_array, y_array, y1_array, x, n):
	index = get_index_to_work_table(x_array, x)
	new_x_array = make_one_work_array(x_array, index, n)
	new_y_array = make_one_work_array(y_array, index, n)
	new_y1_array = make_one_work_array(y1_array, index, n)
	return new_x_array, new_y_array, new_y1_array

def make_ermit_work_tables(x_array, y_array, y1_array):
	new_x_array = []
	new_y_array = []
	new_y1_array = []
	for i in range(len(x_array)):
		new_x_array.append(x_array[i])
		new_x_array.append(x_array[i])
		new_y_array.append(y_array[i])
		new_y_array.append(y_array[i])
		new_y1_array.append(y1_array[i])
		new_y1_array.append(y1_array[i])
	return new_x_array, new_y_array, new_y1_array

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

def ermit_step_of_differences(x_array, y_array, y1_array):
	next_y_array = []
	x_step = len(x_array) - len(y_array) + 1
	for i in range(len(y_array) - 1):
		if (fabs(x_array[i] - x_array[i+x_step]) < EPS):
			difference = y1_array[i]
		else:
			difference = (y_array[i] - y_array[i+1])/(x_array[i] - x_array[i+x_step])
		next_y_array.append(difference)
	return next_y_array

def ermit_find_coef(x_array, y_array, y1_array, n):
	coefs = [y_array[0]]
	cur_n = 0
	while len(y_array)!= 1:
		y_array = ermit_step_of_differences(x_array, y_array, y1_array)
		coefs.append(y_array[0])
		cur_n += 1
		if (cur_n >= n):
			break
	return coefs

def ermit_solve_polinom(x_array, y_array, y1_array, x, n):
	coefs = ermit_find_coef(x_array, y_array, y1_array, n)
	res = coefs[0]
	mnoj = 1
	for i in range(1, len(coefs)):
		mnoj *= (x - x_array[i - 1]) 
		res += coefs[i] * mnoj
	return res

def get_root(x_array, y_array, n):
	x = 0

	index = get_index_to_work_table(x_array, x)
	new_x_array = make_one_work_array(y_array, index, n)
	new_y_array = make_one_work_array(x_array, index, n)
	
	res = newtonian_solve_polinom(new_x_array, new_y_array, x, n)
	return res


def print_table(x_array, y_array, y1_array, cur_x):
	n = 1
	new_x_array, new_y_array, new_y1_array = make_work_tables(x_array, y_array, y1_array, cur_x, n)
	newtonian_solve_polinom(new_x_array, new_y_array, cur_x, n)
	n = n*2
	new_x_array, new_y_array, new_y1_array = make_ermit_work_tables(new_x_array, new_y_array, new_y1_array)
	ermit_solve_polinom(new_x_array, new_y_array, new_y1_array, cur_x, n)
	print("|{:^3}|{:^10}|{:^10}|{:^10}|".format("N", "Ньютон", "Эрмит", "Корень"))

	for i in range(1, MAX_N+1):
		n = i
		new_x_array, new_y_array, new_y1_array = make_work_tables(x_array, y_array, y1_array, cur_x, n)
		newt_res = newtonian_solve_polinom(new_x_array, new_y_array, cur_x, n)
		n = n*2
		new_x_array, new_y_array, new_y1_array = make_ermit_work_tables(new_x_array, new_y_array, new_y1_array)
		ermit_res = ermit_solve_polinom(new_x_array, new_y_array, new_y1_array, cur_x, n)
		root = get_root(x_array, y_array, n)
		print("|{:3d}|{:10f}|{:10f}|{:10f}|".format(n//2, newt_res, ermit_res, root))

X, Y, Y1 = read_file("test_1.txt")	
sort_start_data(X, Y, Y1)
CUR_X = float(input("Введите х: "))
if (CUR_X < X[0] or CUR_X > X[len(X)-1]):
	print("х находится за границами введенной таблицы значений")
else:
	print_table(X, Y, Y1, CUR_X)