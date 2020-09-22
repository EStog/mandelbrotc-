"""
Main file.
Uncomment all commented lines and comment "frame = run()" line (14) to
only plot the results without running the whole experiment.
"""

# import pandas as pd

# from consts import RUN_DATA_FILE
from plotting import plot_results

from running import run

frame = run()

# frame = pd.read_csv(RUN_DATA_FILE)

plot_results(frame)

print()
