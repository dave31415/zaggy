from scaling import scale_date
from zaggy import l1_fit
from seasonality import get_seasonality_matrix


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
                 timescale=(1, 'day'),
                 seasonality_function=None,
                 params=None):
        """
        :param dates: iterable of datetime.date or datetime.datetime objects
        :param y: iterable, the y-values for the time series
        :param timescale: sets the time scale for scaling dates to numbers
                          allows the regularization parameters to stay scale
                          independent
        :param seasonality_function:
        :param params:
        :return:
        """
        self.dates = dates
        self.y = y
        self.timescale = timescale
        self.x = [scale_date(date, self.timescale) for date in dates]
        if seasonality_function is None:
            seasonality_function = lambda x: 0

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
        pass

