from random_time_series import make_random_ts
from zaggy_model import ZaggyModel

doplot = True

if doplot:
    try:
        from matplotlib import pylab as plt
    except ImportError:
        print "Cannot import matplotlib, turning plotting off"
        doplot = False


def run_on_random(num_ts=5, n_points=70, prompt=False):
    n_plots_long = 5
    n_plots_wide = 1
    i = 0
    timescale = (5, 'day')
    params = {'beta_step': 1000,
              'beta_d1': 0.0,
              'beta_d2': 1.0
              }
    for seed in xrange(num_ts):
        print 'seed: %s' % seed
        t, y = make_random_ts(n_points, seed=seed)
        model = ZaggyModel(t, y, timescale=timescale, params=params)
        model.fit()

        if doplot:
            if i % (n_plots_long*n_plots_wide) == 0:
                plt.clf()
            n_plot = (i % (n_plots_long*n_plots_wide)) + 1
            plt.subplot(n_plots_long, n_plots_wide, n_plot)
            plt.plot(t, y)
            plt.plot(t, model.solution['model'])
            if prompt:
                ans = raw_input('ok?:')
                if ans == 'q':
                    return
        i += 1
