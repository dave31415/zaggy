import numpy as np

doplot = False


def make_mock(do_plot=doplot, period=6, sea_amp=0.05, noise=0.0):
    np.random.seed(3733)
    num = 100
    x = np.arange(num)
    y = np.zeros(num)
    y[0:20] = 20.0 + x[0:20] * 1.5
    y[20:50] = y[19] - (x[20:50] - x[19]) * 0.2
    y[50:60] = y[49] + (x[50:60] - x[49]) * 0.47
    y[60:75] = y[59] - (x[60:75] - x[59]) * 2.4
    y[75:] = y[74] + (x[75:] - x[74]) * 2.0
    y = y / y.max()
    y += noise * np.random.randn(num)
    if period > 0:
        seas = np.random.randn(period) * sea_amp
        seas_lookup = {k: v for k, v in enumerate(seas)}
        seasonal_part = np.array([seas_lookup[i % period] for i in x])
        seasonal_part = seasonal_part - seasonal_part.mean()
        y_without_seasonal = y
        y = y + seasonal_part
    else:
        y_without_seasonal = y

    if do_plot:
        from matplotlib import pylab as plt
        plt.clf()
        lab = 'True, period=%s' % period
        plt.plot(x, y_without_seasonal, marker='o', linestyle='-', label=lab, markersize=8, alpha=0.3,color='blue')
        lab = 'True + seasonality, period=%s' % period
        plt.plot(x, y, marker='o', linestyle='-', label=lab, markersize=8, alpha=0.3,color='red')

    np.random.seed(None)
    return {'x': x, 'y': y, 'y_without_seasonal': y_without_seasonal, 'seas_lookup': seas_lookup}