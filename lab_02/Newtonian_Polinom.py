from math import fabs

EPS = 0.00001

MAX_N = 2

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

def make_work_tables(x_array, y_array, x, n):
	index = get_index_to_work_table(x_array, x)
	new_x_array = make_one_work_array(x_array, index, n)
	new_y_array = make_one_work_array(y_array, index, n)
	return new_x_array, new_y_array

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

def print_table(x_array, y_array, cur_x, cur_y, values):
	print("|{:^6}|{:^5}|{:^5}|{:^5}|".format("Nx/Ny", "1", "2", "3"))

	for y_n in range(0, MAX_N + 1):
		print("|{:^6}|".format(y_n + 1), end="")
		for x_n in range(0, MAX_N + 1):
			args = []
			for i in range(len(values)):
				x_current, y_current = make_work_tables(x_array, values[i], cur_x, x_n + 1)
				args.append(newtonian_solve_polinom(x_current, y_current, cur_x, x_n + 1))
			x_current, y_current = make_work_tables(y_array, args, cur_y, y_n + 1)
			res = newtonian_solve_polinom(x_current, y_current, cur_y, y_n + 1)
			print("{:^5}".format(res), end='|')
		print()

x = [0, 1, 2, 3, 4]
y = [0, 1, 2, 3, 4]
means = [[0, 1, 4, 9, 16],
        [1, 2, 5, 10, 17],
        [4, 5, 8, 13, 20],
        [9, 10, 13, 18, 25],
        [16, 17, 20, 25, 32]]
x_zn = float(input())
y_zn = float(input())
print_table(x, y, x_zn, y_zn, means)
