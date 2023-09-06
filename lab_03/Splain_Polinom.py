from math import fabs

EPS = 0.00001

MAX_N = 4

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


def print_table(x_array, y_array, y1_array, cur_x):
	n = 1
	new_x_array, new_y_array, new_y1_array = make_work_tables(x_array, y_array, y1_array, cur_x, n)
	newtonian_solve_polinom(new_x_array, new_y_array, cur_x, n)
	print("|{:^3}|{:^10}|".format("N", "Ньютон"))

	for i in range(1, MAX_N+1):
		n = i
		new_x_array, new_y_array, new_y1_array = make_work_tables(x_array, y_array, y1_array, cur_x, n)
		newt_res = newtonian_solve_polinom(new_x_array, new_y_array, cur_x, n)
		print("|{:3d}|{:10f}|".format(n//2, newt_res))
