from matplotlib import pylab as plt
from mocks import make_mock
from zaggy_model import ZaggyModel
from date_scaling import date_range


def get_mock_with_dates():
    mock = make_mock()
    num = len(mock['x'])
    mock['dates'] = date_range(2015, 1, 2099, 12)[:num]
    return mock


def plot_mock(mock):
    plt.clf()
    plt.plot(mock['dates'], mock['y'], marker='+', color='blue')
    plt.plot(mock['dates'], mock['y_without_seasonal'], color='green',alpha=0.3, linewidth=1)


def plot_model(model):
    plt.plot(model.dates, model.solution['model'], color='red')


def make_simple_plot(params=None):
    mock = get_mock_with_dates()
    plot_mock(mock)
    timescale = (1.0, 'day')
    model = ZaggyModel(mock['dates'], mock['y'], timescale=timescale, params=params)
    model.fit()
    plot_model(model)
    plt.legend()
    return model
