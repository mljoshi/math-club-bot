import sympy
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import transformations
from sympy.printing.latex import latex
from io import BytesIO
from PIL import Image
import random
import math
from datetime import datetime
# SymPy symbol definitions
x = sympy.symbols('x')
y = sympy.symbols('y')
i = sympy.symbols('i')
# i is for summation (in estimating an integral with a Riemann sum)

def simplify(func):
    f = parse_expr(func, transformations='all')
    sympy_ans = sympy.simplify(f)
    return sympy_ans

def point_simplify(func, c):
    f = parse_expr(func, transformations='all')
    sympy_ans = sympy.simplify(f.subs(x, c))
    return sympy_ans

def evaluate(func):
    f = parse_expr(func, transformations='all')
    sympy_ans = sympy.N(f)
    return sympy_ans

def point_evaluate(func, c):
    f = parse_expr(func, transformations='all')
    sympy_ans = sympy.N(f, subs={x: c})
    return sympy_ans

def partial_fraction(func):
    f = parse_expr(func, transformations='all')
    sympy_ans = sympy.apart(f)
    return sympy_ans

def integrate(func, variable_of_integration):
    f = parse_expr(func, transformations='all')
    if (variable_of_integration.lower() == "x"):
        sympy_ans = sympy.integrate(f, x)
    else:
        sympy_ans = sympy.integrate(f, y)
    return sympy_ans

def def_integrate(func, a, b, variable_of_integration):
    a, b = (parse_expr(a), parse_expr(b))
    f = parse_expr(func, transformations='all')
    if (variable_of_integration.lower() == 'x'):
        sympy_ans = sympy.integrate(f, (x, a, b))
    else:
        sympy_ans = sympy.integrate(f, (y, a, b))
    return sympy_ans

def ftc2(func, a, b):
    a, b = (parse_expr(a), parse_expr(b))
    f = parse_expr(func, transformations='all')
    sympy_ans = f.subs(x, b) - f.subs(x, a)
    return sympy_ans

def average_value(func, a, b): # This parse_expr cannot be the best way to go about it but it works
    f = parse_expr(func, transformations='all')
    sympy_ans = sympy.Mul(sympy.integrate(f, (x, parse_expr(a), parse_expr(b))), parse_expr("1/(" + str(b) + "-" + str(a) + ")"))
    return sympy_ans

"""
def est_integral(func, a, b, n): # These parse_expr functions cannot be the best way to go about it but it works
    f = parse_expr(func, transformations='all')
    f = f.subs(x, parse_expr("" + str(a) + "+" + "i*" + "(" + str(b) + "-" + str(a) + ")/" + str(n)))
    sympy_ans = sympy.N(sympy.Mul(sympy.summation(f, (i, 1, n)), parse_expr("(" + str(b) + "-" + str(a) + ")/" + str(n))))
    return sympy_ans
"""

def equal_integrals(func1, func2, n, x1, x2, epsilon): # Assumes continuity of functions within the domain provided
    f = parse_expr(func1, transformations='all')
    g = parse_expr(func2, transformations='all')
    random.seed(datetime.now().timestamp())
    for i in range(n):
        # Random x within the domain of (x1, x2)
        a = (x2-x1)*random.random() + x1
        b = (x2-x1)*random.random() + x1
        comparison = sympy.simplify(sympy.simplify(f.subs(x, b) - f.subs(x, a) - (g.subs(x, b) - g.subs(x, a))))
        #print(comparison)
        try:
            if (comparison > epsilon or comparison < -epsilon):
                return (0,)
        except TypeError:
            return (-1,)
    difference = str(sympy.simplify(sympy.N(f.subs(x, b)) - sympy.N(g.subs(x, b)))) # Python variable scope is interesting with its "function-level" scope as opposed to the typical "block-level" scope
    return (1, difference)

def left_riemann(func, a=0.0, b=1.0, n=10):
    f = parse_expr(func, transformations='all')
    sub_interval = (b-a)/n
    sympy_ans = 0
    # Start at 0 since it's a left riemann sum
    for i in range(n):
        sympy_ans += f.subs(x, a + i * sub_interval)
    sympy_ans *= sub_interval
    return sympy_ans

def right_riemann(func, a=0.0, b=1.0, n=10):
    f = parse_expr(func, transformations='all')
    sub_interval = (b-a)/n
    sympy_ans = 0
    # Start at 1 since it's a right riemann sum
    for i in range(1, n + 1):
        sympy_ans += f.subs(x, a + i * sub_interval)
    sympy_ans *= sub_interval
    return sympy_ans

def mid_riemann(func, a=0.0, b=1.0, n=10):
    f = parse_expr(func, transformations='all')
    sub_interval = (b-a)/n
    sympy_ans = 0
    for i in range(n):
        # Add on sub_interval / 2 to substitution since mid point
        sympy_ans += f.subs(x, a + sub_interval / 2 + i * sub_interval)
    sympy_ans *= sub_interval
    return sympy_ans

def upper_sum(func, a=0.0, b=1.0, n=10):
    f = parse_expr(func, transformations='all')
    sub_interval = (b-a)/n
    sympy_ans = 0
    for i in range(n):
        sympy_ans += maximum_val(f, a + i * sub_interval, a + (i + 1) * sub_interval)
    sympy_ans *= sub_interval
    return sympy_ans

def lower_sum(func, a=0.0, b=1.0, n=10):
    f = parse_expr(func, transformations='all')
    sub_interval = (b-a)/n
    sympy_ans = 0
    for i in range(n):
        sympy_ans += minimum_val(f, a + i * sub_interval, a + (i + 1) * sub_interval)
    sympy_ans *= sub_interval
    return sympy_ans

def disk_method(func, variable_of_integration, a, b, line):
    a, b, line = (parse_expr(a), parse_expr(b), parse_expr(line))
    f = parse_expr("pi*(" + str(line) + "-" + func + ")^2", transformations='all')
    if (variable_of_integration.lower() == "x"):
        sympy_ans = sympy.integrate(f, (x, a, b))
    else:
        sympy_ans = sympy.integrate(f, (y, a, b))
    return sympy_ans

def washer_method(func1, func2, variable_of_integration, a, b, line):
    a, b, line = (parse_expr(a), parse_expr(b), parse_expr(line))
    f = parse_expr("pi*(" + str(line) + "-" + func1 + ")^2-pi*(" + str(line) + "-" + func2 + ")^2", transformations='all')
    if (variable_of_integration.lower() == "x"):
        sympy_ans = sympy.integrate(f, (x, a, b))
    else:
        sympy_ans = sympy.integrate(f, (y, a, b))
    sympy_ans = sympy.functions.Abs(sympy_ans)
    return sympy_ans

def shell_method(func, variable_of_integration, a, b, line, function2):
    a, b, line = (parse_expr(a), parse_expr(b), parse_expr(line))
    if (variable_of_integration.lower() == "x"):
        f = parse_expr("2*pi*(x - " + str(line) + ")*(" + func + " - " + function2 + ")", transformations='all')
        sympy_ans = sympy.integrate(f, (x, a, b))
    else:
        f = parse_expr("2*pi*(y - " + str(line) + ")*(" + func + " - " + function2 + ")", transformations='all')
        sympy_ans = sympy.integrate(f, (y, a, b))
    sympy_ans = sympy.functions.Abs(sympy_ans)
    return sympy_ans

def trapezoid_approximation(func, a, b, n, variable_of_integration):
    f = parse_expr(func, transformations='all')
    a, b = (parse_expr(a), parse_expr(b))
    delta = (b - a) / n
    if (variable_of_integration.lower() == "x"):
        sympy_ans = f.subs(x, a) + f.subs(x, b)
        for i in range(1, n):
            sympy_ans += 2 * f.subs(x, a + i * delta)
    else:
        sympy_ans = f.subs(y, a) + f.subs(y, b)
        for i in range(1, n):
            sympy_ans += 2 * f.subs(y, a + i * delta)
    sympy_ans = sympy_ans * delta / 2
    return sympy_ans, float(sympy_ans)

def simpson_rule(func, a, b, n, variable_of_integration):
    f = parse_expr(func, transformations='all')
    a, b = (parse_expr(a), parse_expr(b))
    delta = (b - a) / n
    if (variable_of_integration.lower() == 'x'):
        sympy_ans = f.subs(x, a) + f.subs(x, b)
        for i in range(1, n // 2 + 1):
            sympy_ans += 4 * f.subs(x, a + 2 * i * delta - delta)
        for i in range(1, n // 2):
            sympy_ans += 2 * f.subs(x, a + 2 * i * delta)
    else:
        sympy_ans = f.subs(y, a) + f.subs(y, b)
        for i in range(1, n // 2 + 1):
            sympy_ans += 4 * f.subs(y, a + 2 * i * delta - delta)
        for i in range(1, n // 2):
            sympy_ans += 2 * f.subs(y, a + 2 * i * delta)
    sympy_ans = sympy_ans * delta / 3
    return sympy_ans, float(sympy_ans)

def arc_length(func, a, b, variable_of_integration):
    f = parse_expr(func, transformations='all')
    a, b = (parse_expr(a), parse_expr(b))
    if (variable_of_integration.lower() == 'x'):
        f = sympy.diff(f, x)
    else:
        f = sympy.diff(f, y)
    g = "sqrt(1 + (" + str(f) + ")^2)"
    g = parse_expr(g, transformations='all')
    if (variable_of_integration.lower() == 'x'):
        sympy_ans = sympy.integrate(g, (x, a, b))
    else:
        sympy_ans = sympy.integrate(g, (y, a, b))
    # Add check for if the function can be converted to float, if not do Simpson's rule for the integral
    if ("Integral" in str(sympy_ans)):
        if (variable_of_integration.lower() == 'x'):
            return (sympy_ans, simpson_rule(str(g), str(a), str(b), 50, 'x')[1])
        else:
            return (sympy_ans, simpson_rule(str(g), str(a), str(b), 50, 'y')[1])
    return (sympy_ans, None)

def euler_method(func, initial_x, initial_y, step_size, n):
    ans_list = []
    f = parse_expr(func, transformations='all')
    for i in range(n):
        m_n = f.subs({x: initial_x, y: initial_y})
        y_n = m_n * step_size + initial_y
        ans_list.append((initial_x + step_size, float(y_n)))
        # Prepare for next iteration
        initial_x += step_size
        initial_y = y_n
    return ans_list

# Find the intersections between two functions on the interval [a, b]. The solution set, interval, and functions are in terms of x
def interval_intersections(func1, func2, a, b):
    a, b = (parse_expr(a), parse_expr(b))
    f = parse_expr(func1 + "-" + func2, transformations='all')
    solution_set = set(sympy.solveset(f, x, sympy.Interval(a, b)))
    return solution_set

def intersections(func1, func2):
    f = parse_expr(func1 + "-" + func2, transformations='all')
    solution_set = set(sympy.solveset(f, x))
    return solution_set

def differentiate(func):
    f = parse_expr(func, transformations='all')
    sympy_ans = sympy.diff(f, x)
    return sympy_ans

def point_differentiate(func, c):
    f = parse_expr(func, transformations='all')
    sympy_ans = sympy.diff(f, x).subs(x, c)
    return sympy_ans

def maximum_val(func, a=0.0, b=1.0):
    f = parse_expr(str(func), transformations='all') # type cast to string since used in another function and parse_expr only works on strings, change so parse_expr is done in main later
    possible_max_x = set(sympy.solveset(sympy.diff(f, x), x, sympy.Interval(a, b)))
    possible_max_x.add(a)
    possible_max_x.add(b)
    possible_max_val = [f.subs(x, x_val) for x_val in possible_max_x]
    sympy_ans = max(possible_max_val)
    return sympy_ans

def minimum_val(func, a=0.0, b=1.0):
    f = parse_expr(str(func), transformations='all') # type cast to string since used in another function and parse_expr only works on strings, change so parse_expr is done in main later
    possible_min_x = set(sympy.solveset(sympy.diff(f, x), x, sympy.Interval(a, b)))
    possible_min_x.add(a)
    possible_min_x.add(b)
    possible_min_val = [f.subs(x, x_val) for x_val in possible_min_x]
    sympy_ans = min(possible_min_val)
    return sympy_ans

def image_processing(sympy_ans):
    obj = BytesIO()
    sympy.preview(sympy_ans, viewer='BytesIO', outputbuffer=obj)
    im = Image.open(obj)
    resized_im = im.resize((int(im.size[0] * 2.5), int(im.size[1] * 2.5)))
    return resized_im