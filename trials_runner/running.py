import operator
import random
import subprocess as sp
import time
from datetime import datetime, timedelta
from itertools import product

import pandas as pd

from consts import IMPLEMENTATION_LABEL, PROCESSORS_AMOUNT_LABEL, ITER_LIMIT_LABEL, \
    RUN_TIME_LABEL, SPEEDUP_LABEL, EFFICIENCY_LABEL, RUN_DATA_FILE, INFO_FILE, \
    SEP, STATUS_COMMAND, WAIT_TIME, SEQUENTIAL_PROGRAM, PARALLEL_PROGRAMS, \
    TRIALS_AMOUNT, ITER_LIMITS_AMOUNT, ITER_LIMITS, PROGRAMS, SHORT_SEP, PROCESSORS_AMOUNTS, \
    PROCESSORS_AMOUNTS_AMOUNT, PARALLEL_PROGRAMS_AMOUNT

INIT_TIME = datetime.now()
REFERENCE_ITER_LIMIT = ITER_LIMITS[0]


def get_estimated_time():
    """
    Optimistically estimate experiment execution time.
    Running this function does not affect the experiment outcome.
    """
    command = SEQUENTIAL_PROGRAM.command.format(iter_limit=REFERENCE_ITER_LIMIT)
    reference_runtime = float(sp.run(command, shell=True,
                                     universal_newlines=True,
                                     check=True, stdout=sp.PIPE).stdout)
    estimated_time_of_sequential = 0
    for iter_limit in ITER_LIMITS:
        estimated_time_of_sequential += reference_runtime * iter_limit / REFERENCE_ITER_LIMIT + WAIT_TIME

    estimated_time_of_parallel = 0
    for p, iter_limit in product(PROCESSORS_AMOUNTS, ITER_LIMITS):
        estimated_time_of_parallel += \
            (reference_runtime * iter_limit / REFERENCE_ITER_LIMIT / p + WAIT_TIME) * PARALLEL_PROGRAMS_AMOUNT

    estimated_time = (estimated_time_of_sequential + estimated_time_of_parallel) * TRIALS_AMOUNT
    return timedelta(seconds=estimated_time)


print()
TOTAL_RUNNING_AMOUNT = TRIALS_AMOUNT * PARALLEL_PROGRAMS_AMOUNT * ITER_LIMITS_AMOUNT * PROCESSORS_AMOUNTS_AMOUNT + \
    TRIALS_AMOUNT*ITER_LIMITS_AMOUNT
print(f'Total runs to process: {TOTAL_RUNNING_AMOUNT}')
processed = 0

TOTAL_ESTIMATED_TIME = get_estimated_time()
print(f'Total estimated time:  {TOTAL_ESTIMATED_TIME}')


def wait():
    print(f'Waiting {WAIT_TIME} seconds...')
    time.sleep(WAIT_TIME)


def get_runtime(program, p, iter_limit):
    if program is SEQUENTIAL_PROGRAM:
        command = program.command.format(iter_limit=iter_limit)
    else:
        command = program.command.format(iter_limit=iter_limit, p=p)
    wait()
    print(f'Running "{command}" ...')
    runtime = float(sp.run(command, shell=True,
                           universal_newlines=True,
                           check=True, stdout=sp.PIPE).stdout)
    return runtime


def save_status():
    print(f"Saving machine status to '{INFO_FILE}'... ({STATUS_COMMAND})")
    s = sp.run(STATUS_COMMAND, shell=True, check=True,
               stdout=sp.PIPE, universal_newlines=True).stdout
    with open(INFO_FILE, 'w') as f:
        f.write(s)


def get_final_result(results):
    results_dict = {
        IMPLEMENTATION_LABEL: results[0],
        PROCESSORS_AMOUNT_LABEL: results[1],
        ITER_LIMIT_LABEL: results[2],
        RUN_TIME_LABEL: results[3],
        SPEEDUP_LABEL: [],
        EFFICIENCY_LABEL: []
    }

    for i, program in enumerate([SEQUENTIAL_PROGRAM] + PARALLEL_PROGRAMS):
        for j in range(PROCESSORS_AMOUNTS_AMOUNT):
            for k in range(ITER_LIMITS_AMOUNT):
                speedup = results[-1][k] / results[-1][
                    i * PROCESSORS_AMOUNTS_AMOUNT * ITER_LIMITS_AMOUNT + j * ITER_LIMITS_AMOUNT + k]
                results_dict[SPEEDUP_LABEL].append(speedup)
                results_dict[EFFICIENCY_LABEL].append(speedup / (j + 1))

    return results_dict


def print_info(trial_number):
    print(SHORT_SEP)
    elapsed_time = datetime.now() - INIT_TIME
    remaining_time = TOTAL_ESTIMATED_TIME - elapsed_time
    if remaining_time < timedelta(seconds=0):
        remaining_time = timedelta(seconds=0)
    print(SHORT_SEP)
    print(f'Elapsed time:     {elapsed_time}')
    print(f'Remaining time:   {remaining_time}')
    print(f'Trial number:     {trial_number}')
    print(f'Remaining trials: {TRIALS_AMOUNT - trial_number}')
    print(f'Runs processed:   {processed}')
    print(f'Runs remaining:   {TOTAL_RUNNING_AMOUNT - processed}')
    print(SHORT_SEP)


def make_trial(trial_number):
    global processed
    print(SEP)
    print(f'Running trial {trial_number}')
    print(SEP)
    implementations, processors_amounts, iter_limits, run_times = [], [], [], []
    sequential_runs = {}

    random.seed()

    pxpxi = random.sample(
        list(product(PROGRAMS, PROCESSORS_AMOUNTS, ITER_LIMITS)),
        k=(PARALLEL_PROGRAMS_AMOUNT+1) * PROCESSORS_AMOUNTS_AMOUNT * ITER_LIMITS_AMOUNT
    )

    for program, p, iter_limit in pxpxi:
        implementations.append(program)
        processors_amounts.append(p)
        iter_limits.append(iter_limit)
        if program is not SEQUENTIAL_PROGRAM or iter_limit not in sequential_runs:
            print(f'processors amount, iter_limit = {p}, {iter_limit}')
            runtime = get_runtime(program, p, iter_limit)
            print(f'Execution time: {runtime}')
            processed += 1
            print_info(trial_number)
            if program is SEQUENTIAL_PROGRAM:
                sequential_runs[iter_limit] = runtime
        else:
            runtime = sequential_runs[iter_limit]
        run_times.append(runtime)

    return list(zip(*sorted(
        zip(implementations, processors_amounts, iter_limits, run_times),
        key=lambda a: (a[0].index, a[1], a[2], a[3])
    )))


def get_run():
    save_status()
    results = make_trial(1)

    for i in range(2, TRIALS_AMOUNT + 1):
        trial_results = make_trial(i)
        results[-1] = list(map(operator.add, results[-1], trial_results[-1]))

    results[-1] = list(map(lambda x: x / TRIALS_AMOUNT, results[-1]))
    execution_results = get_final_result(results)

    print(f'Experiment finished.')
    print(f'Elapsed time:   {datetime.now() - INIT_TIME}')
    print(f'Estimated time: {TOTAL_ESTIMATED_TIME}')

    return execution_results


def run():
    execution_results = get_run()

    print(f'Saving data to {RUN_DATA_FILE}...')
    frame = pd.DataFrame(execution_results)

    frame.to_csv(RUN_DATA_FILE)

    return frame
