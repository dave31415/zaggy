import matrix_utils as mu
import l1
import numpy as np
from cvxopt import spmatrix, matrix, sparse


def l1_fit(index, y, beta_d2=1.0, beta_d1=1.0, beta_seasonal=1.0,
           beta_step=1000.0, growth=0.0, seasonality_matrix=None):
    """
    Least Absolute Deviation Time Series fitting function
           lower-level than version operating on actual dates
    :param index: ndarray, index of numeric x-values representing time
    :param y: ndarray, the time-series y-values
    :param beta_d2: L1 regularization parameter on the second derivative
    :param beta_d1: L1 regularization parameter on the first derivative
    :param beta_seasonal: L1 regularization parameter on the
           seasonal components
    :param beta_step: L1 regularization parameter on the
           step-function components
    :param growth: the default growth rate that is regularized toward
           default 0
    :param seasonality_matrix:
           matrix which maps seasonality variables onto the index of data points
           allows the problem to be written in purely matrix form
           comes from get_seasonality_matrix function
    :return:
    """

    # print "beta_d2: %s" % beta_d2
    # print "beta_seasonal: %s" % beta_seasonal

    assert isinstance(y, np.ndarray)
    assert isinstance(index, np.ndarray)
    #x must be integer type for seasonality to make sense
    #assert index.dtype.kind == 'i'
    # dimensions
    n = len(y)
    m = n-2
    p = seasonality_matrix.size[1]

    ys, y_min, y_max = mu.scale_numpy(y)

    # set up matrices
    d1 = mu.get_first_derivative_matrix_nes(index)
    d2 = mu.get_second_derivative_matrix_nes(index)
    h = mu.get_step_function_matrix(n)
    t = mu.get_T_matrix(p)
    q = seasonality_matrix * t

    zero = mu.zero_spmatrix
    ident = mu.identity_spmatrix
    gvec = spmatrix(growth, range(m), [0]*m)
    zero_m = spmatrix(0.0, range(m), [0]*m)
    zero_p = spmatrix(0.0, range(p), [0]*p)
    zero_n = spmatrix(0.0, range(n), [0]*n)

    # allow step-function regularization to change at some points
    # is this really needed?

    step_reg = mu.get_step_function_reg(n, beta_step)

    # define F_matrix from blocks like in white paper
    # so that the problem can be stated as a standard LAD problem
    # and solvable with the l1 program

    F_matrix = sparse([
        [ident(n), -beta_d1*d1, -beta_d2*d2, zero(p, n), zero(n)],
        [q, zero(m, p-1), zero(m, p-1), -beta_seasonal*t, zero(n, p-1)],
        [h, zero(m, n), zero(m, n), zero(p, n), step_reg]
    ])

    # convert to sparse matrix
    w_vector = sparse([
        mu.np2spmatrix(ys), gvec, zero_m, zero_p, zero_n
    ])

    # solve LAD problem and convert back to numpy array
    solution_vector = np.asarray(l1.l1(matrix(F_matrix), matrix(w_vector))).squeeze()

    #separate into components
    base = solution_vector[0:n]
    seasonal_parameters = solution_vector[n:n+p-1]
    step_jumps = solution_vector[n+p-1:]
    #scale back to original
    if y_max > y_min:
        scaling = y_max - y_min
    else:
        scaling = 1.0

    base = base * scaling + y_min
    seasonal_parameters *= scaling
    step_jumps *= scaling
    seasonal_component = np.asarray(q*matrix(seasonal_parameters)).squeeze()
    step_component = np.asarray(h*matrix(step_jumps)).squeeze()
    model_without_seasonal = base + step_component
    model = model_without_seasonal + seasonal_component

    solution = {'base': base,
                'seasonal_component': seasonal_component,
                'step_component': step_component,
                'model': model,
                'model_without_seasonal': model_without_seasonal,
                'step_jumps': step_jumps,
                'seasonal_parameters': seasonal_parameters}

    return solution

