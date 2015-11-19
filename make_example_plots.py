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
    plt.plot(mock['dates'], mock['y'], marker='+', color='blue',
             label='data', markersize=9)
    plt.plot(mock['dates'], mock['y_without_seasonal'],
             color='green', alpha=0.6, linewidth=1,
             label='model without seasonal')


def plot_model(model):
    plt.plot(model.dates, model.solution['model'], color='red',
             label='model')


def make_simple_plot(params=None):
    mock = get_mock_with_dates()
    plot_mock(mock)
    timescale = (1.0, 'month')
    model = ZaggyModel(mock['dates'], mock['y'], timescale=timescale,
                       params=params)
    model.fit()
    plot_model(model)
    plt.legend()
    return model


def make_extrapolatad_plot(params=None):
    mock = get_mock_with_dates()
    plot_mock(mock)
    timescale = (1.0, 'month')
    model = ZaggyModel(mock['dates'], mock['y'], timescale=timescale,
                       params=params)
    model.fit()
    plot_model(model)

    dates = date_range(2022, 1, 2024, 12)
    results = model.predict(dates)
    plt.plot(dates, results, color='orange', alpha=0.7, marker='d',
             label='predictions')

    dates = date_range(2014, 1, 2016, 1)
    results = model.predict(dates)
    plt.plot(dates, results, color='orange', alpha=0.7, marker='s',
             label='predictions (earlier)')

    plt.legend(loc='upper left')
    return model