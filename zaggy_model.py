from date_scaling import scale_date
from zaggy import l1_fit
from seasonality import get_seasonality_matrix
import numpy as np


def default_params():
    return {"beta_d1": 0.0,
            "beta_d2": 1.0,
            "beta_seasonal": 1.0,
            "beta_step": 5.0,
            "growth": 0.0}


class ZaggyModel(object):
    """
    A zaggy time series model
    """

    def __init__(self, dates, y,
                 timescale=(1, 'month'),
                 seasonality_function=None,
                 params=None):
        """
        Instantiate and initialize the object
        :param dates: iterable of datetime.date or datetime.datetime objects
        :param y: iterable, the y-values for the time series
        :param timescale: sets the time scale for scaling dates to numbers
                          allows the regularization parameters to stay scale
                          independent
        :param seasonality_function: a function that maps dates to an index
               pertaining to seasonality variables (zero indexed)
               example: lambda date: date.month-1
        :param params: a dictionary of overrides for default parameters,
               mostly regularization parameters, see default_params
        :return: an object instance
        """
        self.dates = np.array(dates)
        self.y = np.array(y)
        # scale the dates to an index
        self.timescale = timescale
        self.x = np.array([scale_date(date, self.timescale) for date in dates])
        if seasonality_function is None:
            # TODO: does it make sense to have a default?
            seasonality_function = lambda date: date.month - 1

        # calculate the seasonality matrix, this combined with the
        # index 'x' allows us to forget about dates and call the
        # date agnostic fit function

        self.seasonality_matrix = get_seasonality_matrix(dates,
                                                         seasonality_function)
        self.solution = None
        self.params = default_params()

        if params is not None:
            # override any parameters handed in with
            # params dictionary
            for key, value in params.items():
                self.params[key] = value

    def fit(self):
        self.solution = l1_fit(self.x,
                               self.y,
                               beta_d1=self.params['beta_d1'],
                               beta_d2=self.params['beta_d2'],
                               beta_seasonal=self.params['beta_seasonal'],
                               beta_step=self.params['beta_step'],
                               growth=self.params['growth'],
                               step_permissives=None,
                               seasonality_matrix=self.seasonality_matrix)

    def predict(self, dates):
        if self.solution is None:
            raise ValueError('Solution is not present, must first call fit')
        # calculate the model at the dates, not implemented yet
        pass

