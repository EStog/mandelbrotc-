import os.path
from functools import reduce

import seaborn as sb

from consts import IMPLEMENTATION_LABEL, PROCESSORS_AMOUNT_LABEL, ITER_LIMIT_LABEL, RUN_TIME_LABEL, \
    SPEEDUP_LABEL, EFFICIENCY_LABEL, RUN_DATA_DIR, SEP, PLOTTING_MARKERS, PLOTTING_COL_WRAP


def plot_y_per_col(dataframe, x, y, col, col_wrap, file_name, legend):
    g = sb.factorplot(x=x, y=y, hue=IMPLEMENTATION_LABEL, col=col,
                      col_wrap=col_wrap, kind='point',
                      legend=legend,
                      data=dataframe[[IMPLEMENTATION_LABEL, x, y, col]],
                      markers=PLOTTING_MARKERS)
    indexes = sorted(set(dataframe[x].values))
    char_amount = reduce(lambda a, b: a + len(str(b)), indexes, 0)
    step = char_amount // 16
    if step > 0:
        for i in range(len(indexes)):
            if i != 0 and i % step != 0:
                indexes[i] = ""
        g.set_xticklabels(indexes)
    print(f'Saving to {file_name}...')
    g.savefig(file_name)


def plot_measure(dataframe, measure_label):
    print(f'Plotting {measure_label} per processors amount...')
    plot_y_per_col(dataframe, ITER_LIMIT_LABEL, measure_label, PROCESSORS_AMOUNT_LABEL,
                   PLOTTING_COL_WRAP,
                   os.path.join(RUN_DATA_DIR, f'{measure_label.replace(" ", "_")}_per_processors_amount.svg'),
                   legend=True)

    print(f'Plotting {measure_label} per iteration limit...')
    plot_y_per_col(dataframe, PROCESSORS_AMOUNT_LABEL, measure_label, ITER_LIMIT_LABEL,
                   PLOTTING_COL_WRAP,
                   os.path.join(RUN_DATA_DIR, f'{measure_label.replace(" ", "_")}_per_iteration_limit.svg'),
                   legend=True)


def plot_results(dataframe):
    print(SEP)
    sb.set()
    sb.set_context('poster', rc={'lines.markersize': 3, 'lines.linewidth': 1.5})
    sb.set_style('whitegrid', {'axes.linewidth': 1.5, 'legend.frameon': True})
    sb.set_palette('hls')
    plot_measure(dataframe, RUN_TIME_LABEL)
    plot_measure(dataframe, SPEEDUP_LABEL)
    plot_measure(dataframe, EFFICIENCY_LABEL)
