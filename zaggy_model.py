from date_scaling import scale_date
from zaggy import l1_fit
from seasonality import get_seasonality_matrix
import numpy as np
from scipy.interpolate import interp1d

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
        self.x_min = min(self.x)
        self.x_max = max(self.x)
        if seasonality_function is None:
            # TODO: does it make sense to have a default?
            seasonality_function = lambda the_date: the_date.month - 1
        self.seasonality_function = seasonality_function

        # calculate the seasonality matrix, this combined with the
        # index 'x' allows us to forget about dates and call the
        # date agnostic fit function

        self.seasonality_matrix = get_seasonality_matrix(dates,
                                                         seasonality_function)
        self.solution = None
        self.slope = None
        self.offset = None
        self.seasonal = None
        self.params = default_params()

        # dummy functions for now, replace after fit
        self.interpolate = lambda x: None
        self.extrapolate_without_seasonal = lambda x: None

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
                               seasonality_matrix=self.seasonality_matrix)

        y2 = self.solution['base'][-1]
        y1 = self.solution['base'][-2]
        x2 = self.x[-1]
        x1 = self.x[-2]

        self.slope = (y2 - y1) / float(x2 - x1)
        self.offset = y2 - self.slope * x2

        # fill in the seasonal parameters
        # remember that the last one is 1-sum_of_rest
        # as they sum to zero
        seasonal_params = self.solution['seasonal_parameters']
        sum_seasonal = seasonal_params.sum()
        self.seasonal = np.array(list(seasonal_params) + [-sum_seasonal])

        # set this function for interpolating
        self.interpolate = interp1d(self.x, self.solution['model'])
        self.extrapolate_without_seasonal = lambda new_x: self.offset + self.slope * new_x

    def predict(self, dates):
        if self.solution is None:
            raise ValueError('Solution is not present, must first call fit')

        # set the result to zero by default, points before the
        # first data point will remain zero

        result = np.zeros(len(dates))
        x = np.array([scale_date(date, self.timescale) for date in dates])

        # do the interpolation for the internal region
        interpolate_region = (x >= self.x_min) & (x <= self.x_max)
        result[interpolate_region] = self.interpolate(x[interpolate_region])

        # do the extrapolation beyond the last data point
        extrapolate_region = x > self.x_max
        x_extrap = x[extrapolate_region]
        dates_extrap = np.array(dates)[extrapolate_region]
        non_seasonal_extrap = np.array([self.extrapolate_without_seasonal(xx)
                                        for xx in x_extrap])

        seasonal_indices_extrap = [self.seasonality_function(date)
                                   for date in dates_extrap]
        seasonal_extrap = np.array([self.seasonal[i] for i in seasonal_indices_extrap])

        extrapolated = non_seasonal_extrap + seasonal_extrap
        result[extrapolate_region] = extrapolated
        return result






