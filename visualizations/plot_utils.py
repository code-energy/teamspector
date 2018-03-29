import matplotlib
matplotlib.use('Agg')

def plot_config(scale_h=1):
    # Calculating optimum image size as per http://goo.gl/TDARwl.
    fig_width_pt = 240
    inches_per_pt = 1/72.27
    golden_mean = .6180339
    fig_width = fig_width_pt*inches_per_pt
    fig_height = fig_width*golden_mean*scale_h
    fig_size = [fig_width, fig_height]
    params = {'backend': 'ps',
              'axes.labelsize': 6.5,
              'font.size': 6.5,
              'legend.fontsize': 6.5,
              'xtick.labelsize': 6.5,
              'ytick.labelsize': 6.5,
              'text.usetex': True,
              'figure.figsize': fig_size}
    matplotlib.rcParams.update(params)
