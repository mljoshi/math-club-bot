from math_evaluations import *
import sympy
import math
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.sympy_parser import transformations
from sympy.printing.latex import latex
import random
x = sympy.symbols('x')
y = sympy.symbols('y')
i = sympy.symbols('i')

def run_tests():
    # Test simplify function
    expression = "2x + x - 3"
    result = simplify(expression)
    assert result == 3*x - 3

    # Test point_simplify function
    expression = "2x + x - 3"
    point_result = point_simplify(expression, 2)
    assert point_result == 3

    # Test evaluate function
    expression = "(2x + x)/x"
    eval_result = evaluate(expression)
    assert eval_result == 3

    # Test point_evaluate function
    expression = "2x + x - 3"
    point_eval_result = point_evaluate(expression, 2)
    assert point_eval_result == 3

    # Test partial_fraction function
    expression = "(x + 3)/(x^2 - 1)"
    partial_frac_result = partial_fraction(expression)
    assert partial_frac_result == 2/(x - 1) - 1/(x + 1)

    # Test integrate function
    expression = "x^2 + x"
    integrate_result = integrate(expression, "x")
    assert integrate_result == x**3/3 + x**2/2
    expression = "y^2 + y"
    integrate_result = integrate(expression, "y")
    assert integrate_result == y**3/3 + y**2/2

    # Test def_integrate function
    expression = "x^2 + 3sin(x)"
    def_integrate_result = def_integrate(expression, "0", "2", "x")
    assert math.isclose(def_integrate_result, 6.915107176308094, rel_tol=1e-5)
    expression = "y^2 + 3sin(y)"
    def_integrate_result = def_integrate(expression, "0", "2", "y")
    assert math.isclose(def_integrate_result, 6.915107176308094, rel_tol=1e-5)

    # Test double_integrate function
    expression = "1 + xy"
    double_integrate_result = double_integrate(expression, "x", "0", "y", "0", "1")
    assert double_integrate_result == 5/8
    expression = "x * cos(y)"
    double_integrate_result = double_integrate(expression, "y", "0", "x^2", "0", "1")
    assert math.isclose(double_integrate_result, 0.229848847, rel_tol=1e-5)

    # Test ftc2 function
    expression = "3sin(2x)"
    ftc2_result = ftc2(expression, "pi/12", "pi/4")
    assert ftc2_result == 3/2

    # Test average_value function
    expression = "x^3 + 3"
    average_value_result = average_value(expression, "1", "6")
    assert average_value_result == 271/4

    # Test equal_integrals function
    expression1 = "ln(2x)"
    expression2 = "ln(x)"
    equal_integrals_result = equal_integrals(expression1, expression2, 100, 0, 2, 1e-5)
    assert equal_integrals_result[0] == 1
    assert math.isclose(float(equal_integrals_result[1]), 0.69314718056, rel_tol=1e-5)
    expression1 = "2x"
    expression2 = "3x"
    equal_integrals_result = equal_integrals(expression1, expression2, 100, 0, 2, 1e-5)
    assert equal_integrals_result == (0,)

    # Test left_riemann function
    expression = "4cos(x)"
    left_riemann_result = left_riemann(expression, 0.0, 1.57079632679, 4)
    assert math.isclose(left_riemann_result, 4.73386137119753, rel_tol=1e-5)

    # Test right_riemann function
    expression = "4cos(x)"
    right_riemann_result = right_riemann(expression, 0.0, 1.57079632679, 4)
    assert math.isclose(right_riemann_result, 3.16306503616296, rel_tol=1e-5)

    # Test mid_riemann function
    expression = "11cos(x^2)"
    mid_riemann_result = mid_riemann(expression, 0.0, 1.0, 8)
    assert math.isclose(mid_riemann_result, 9.9618195, rel_tol=1e-5)

    # Test upper_sum function
    expression = "2 + sin(x)"
    upper_sum_result = upper_sum(expression, 0.0, 3.14159265358979323846264, 8)
    assert math.isclose(upper_sum_result, 8.65011599082386, rel_tol=1e-5)

    # Test lower_sum function
    expression = "2 + sin(x)"
    lower_sum_result = lower_sum(expression, 0.0, 3.14159265358979323846264, 8)
    assert math.isclose(lower_sum_result, 7.86471782742641, rel_tol=1e-5)

    # Test disk_method function
    expression = "2*sqrt(5y)"
    disk_method_result = disk_method(expression, "y", "0", "7", "0")
    assert math.isclose(disk_method_result, 1539.38040026, rel_tol=1e-5)

    # Test washer_method function
    expression1 = "3+sec(x)"
    expression2 = "5"
    washer_method_result = washer_method(expression1, expression2, "x", "-pi/3", "pi/3", "3")
    assert math.isclose(washer_method_result, 15.4361489, rel_tol=1e-5)

    # Test shell_method function
    expression = "10x"
    expression2 = "5x^2"
    shell_method_result = shell_method(expression, "x", "0", "2", "0", expression2)
    assert math.isclose(shell_method_result, 41.887902, rel_tol=1e-5)
    expression = "(64y)^(1/3)"
    expression2 = "8"
    shell_method_result = shell_method(expression, "y", "0", "8", "8", expression2)
    assert math.isclose(shell_method_result, 574.462657, rel_tol=1e-5)

    # Test trapezoid_approximation function
    expression = "11cos(x^2)"
    trapezoid_approx_result, trapezoid_approx_float_result = trapezoid_approximation(expression, "0", "1", 8, "x")
    assert math.isclose(trapezoid_approx_float_result, 9.925661277853376, rel_tol=1e-5)
    expression = "11cos(y^2)"
    trapezoid_approx_result, trapezoid_approx_float_result = trapezoid_approximation(expression, "0", "1", 8, "y")
    assert math.isclose(trapezoid_approx_float_result, 9.925661277853376, rel_tol=1e-5)

    # Test simpson_rule function
    expression = "10sin(x)"
    simpson_rule_result, simpson_rule_float_result = simpson_rule(expression, "0", "pi", 10, "x")
    assert math.isclose(simpson_rule_float_result, 20.00109517315004, rel_tol=1e-5)
    expression = "10sin(y)"
    simpson_rule_result, simpson_rule_float_result = simpson_rule(expression, "0", "pi", 10, "y")
    assert math.isclose(simpson_rule_float_result, 20.00109517315004, rel_tol=1e-5)

    # Test arc_length function
    expression = "1/3*sqrt(y)*(y-3)"
    arc_length_result = arc_length(expression, "9", "25", "y")
    assert arc_length_result[0] == 104/3 or math.isclose(arc_length_result[1], 34.6666667, rel_tol=1e-5)

    # Test euler_method function
    expression = "y-2x"
    euler_method_result = euler_method(expression, 4, 0, 0.5, 4)
    assert euler_method_result == [(4.5, -4.0), (5.0, -10.5), (5.5, -20.75), (6.0, -36.625)]

    # Test interval_intersections function
    func1 = "x^2"
    func2 = "2x"
    interval_intersections_result = interval_intersections(func1, func2, "1", "4")
    assert interval_intersections_result == {2}

    # Test intersections function
    func1 = "x^2"
    func2 = "2x"
    intersections_result = intersections(func1, func2)
    assert intersections_result == {0, 2}

    # Test differentiate function
    expression = "x^2"
    diff_result = differentiate(expression)
    assert diff_result == 2*x

    # Test point_differentiate function
    expression = "x^2"
    point_diff_result = point_differentiate(expression, 2)
    assert point_diff_result == 4

    # Test maximum_val function
    expression = "x^2"
    max_val_result = maximum_val(expression, 0, 2)
    assert max_val_result == 4

    # Test minimum_val function
    expression = "x^2"
    min_val_result = minimum_val(expression, 0, 2)
    assert min_val_result == 0

    print("All tests passed")

if __name__ == "__main__":
    run_tests()