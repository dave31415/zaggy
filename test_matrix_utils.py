import numpy as np
import cvxopt
import matrix_utils as mu


doplot = False

if doplot:
    try:
        from matplotlib import pylab as plt
    except ImportError:
        print "Cannot import matplotlib, turning plotting off"
        doplot = False


def test_second_derivative_nes_agrees_with_es():
    #should agree with regularly spaced version when regularly spaced
    n = 13
    D2 = mu.get_second_derivative_matrix(n)
    D2_with_gaps = mu.get_second_derivative_matrix_nes(range(n))
    diff = D2 -D2_with_gaps
    assert max(abs(diff)) < 1e-13


def test_first_derivative_nes_on_quadratic():
    #should agree with regularly spaced version when regularly spaced
    n = 12
    x = np.arange(n)*1.0
    x = x[np.array([1, 2, 5, 9, 11])]
    y = 3.0*x*x + 5.0*x + 99.5
    expected = cvxopt.matrix([6.0*xxx+5.0 for xxx in [2.0, 5.0, 9.0]])
    F = mu.get_first_derivative_matrix_nes(x)
    deriv1 = F*cvxopt.matrix(y)
    diff = deriv1 - expected
    assert max(abs(diff)) < 1e-13


def test_second_derivative_nes_on_quadratic():
    #should agree with regularly spaced version when regularly spaced
    n = 12
    x = np.arange(n)*1.0
    x = x[np.array([1, 2, 5, 9, 11])]
    y = 3.0*x*x + 5.0*x + 99.5
    expected = cvxopt.matrix([6.0 for xxx in [2.0, 5.0, 9.0]])
    F = mu.get_second_derivative_matrix_nes(x)
    deriv2 = F*cvxopt.matrix(y)
    diff = deriv2 - expected
    assert max(abs(diff)) < 1e-13


def test_first_derivative_nes_agrees_with_es():
    #should agree with regularly spaced version when regularly spaced
    n = 13
    F = mu.get_first_derivative_matrix(n)
    F_with_gaps = mu.get_first_derivative_matrix_nes(range(n))
    diff = F -F_with_gaps
    print F
    print F_with_gaps
    max_diff = max(abs(diff))
    print max_diff
    assert max_diff < 1e-13


def test_first_derivative_nes_is_constant_for_line():
    n = 13
    x = np.arange(n)
    F = mu.get_first_derivative_matrix_nes(x)
    xx = cvxopt.matrix(x)
    slope = F*xx
    slope_expected = [1.0]*11
    slope_expected = cvxopt.matrix(slope_expected)
    assert max(abs(slope-slope_expected)) < 1e-13

    #add some gaps, still should be unit slope
    x_with_gaps = x[np.array([1, 4, 5, 9, 11])]
    F = mu.get_first_derivative_matrix_nes(x_with_gaps)
    xx = cvxopt.matrix(x_with_gaps)*3.0+9.5
    slope = F*xx
    slope_expected = [3.0]*(len(x_with_gaps)-2)
    slope_expected = cvxopt.matrix(slope_expected)
    assert max(abs(slope-slope_expected)) < 1e-13


def test_second_derivative_nes_is_zero_for_line():
    n = 13
    x = np.arange(n)
    x_with_gaps = x[np.array([1, 4, 5, 9, 11])]
    D = mu.get_second_derivative_matrix_nes(x_with_gaps)
    slope = D*cvxopt.matrix(x_with_gaps)
    assert max(abs(slope)) < 1e-13


def test_get_B_matrix_nes_aggrees_with_es():
    n = 27
    period = 5
    B_nes = mu.get_B_matrix_nes(np.arange(n), period)
    B_es = mu.get_B_matrix(n, period)

    diff = B_nes-B_es
    max_diff = max(abs(diff))
    assert max_diff < 1e-13


def test_get_B_matrix_nes_on_gap():
    x = np.array([0, 2, 3, 5])
    period = 3
    B_nes = mu.get_B_matrix_nes(x, period)
    expected_matrix = [[1, 0, 0], [0, 0, 1], [1, 0, 0], [0, 0, 1]]
    expected_result = cvxopt.sparse(cvxopt.matrix(expected_matrix).T)
    assert max(B_nes - expected_result) < 1e-13


def test_get_step_function_reg():
    reg = mu.get_step_function_reg(5, 8.0)
    for i in range(5):
        for j in range(5):
            if i != j:
                assert reg[i, j] == 0.0
            else:
                assert reg[i, j] == -8.0
