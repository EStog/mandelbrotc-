import os.path

from util import Program

ITER_LIMITS = [1, 2, 3, 4]  # [100, 1000, 10000, 100000]
ITER_LIMITS_AMOUNT = len(ITER_LIMITS)

TRIALS_AMOUNT = 3
WAIT_TIME = 1

PROCESSORS_AMOUNTS = [1, 2, 4, 8]
PROCESSORS_AMOUNTS_AMOUNT = len(PROCESSORS_AMOUNTS)

CODE_DIR = '../code/'

SEQUENTIAL_PROGRAM = Program(
    name='sequential',
    command=f'{os.path.join(CODE_DIR, "mandelbrot_sequential/build/mandelbrot_sequential")} {{iter_limit}}',
    index=0
)

OMP_SCHEDULES = ('static', 'dynamic', 'guided')

PARALLEL_PROGRAMS = [
    Program(
        name='MPI (send-recv)',
        command='lamboot -b -H && '
                f'mpirun -np {{p}} '
                f'{os.path.join(CODE_DIR, "mandelbrot_mpi_send_recv/build/mandelbrot_mpi_send_recv {iter_limit}")} && '
                'lamhalt -H',
        index=1
    ),
    Program(
        name='MPI (gather)',
        command='lamboot -b -H && '
                f'mpirun -np {{p}} '
                f'{os.path.join(CODE_DIR, "mandelbrot_mpi_gather/build/mandelbrot_mpi_gather {iter_limit}")} && '
                'lamhalt -H',
        index=2
    ),
    *[
        Program(
            name=f'OMP ({s})',
            command=f'OMP_NUM_THREADS={{p}} OMP_SCHEDULE={s} '
                    f'{os.path.join(CODE_DIR, "mandelbrot_openmp/build/mandelbrot_openmp")} {{iter_limit}}',
            index=i + 3
        ) for i, s in enumerate(OMP_SCHEDULES)
    ]
]

PROGRAMS = [SEQUENTIAL_PROGRAM] + PARALLEL_PROGRAMS

PARALLEL_PROGRAMS_AMOUNT = len(PARALLEL_PROGRAMS)

PLOTTING_MARKERS = ['s', 'o', 'v', '*', 'x', '+']
PLOTTING_COL_WRAP = 4

RUN_DATA_DIR = '../data'
try:
    os.mkdir(RUN_DATA_DIR)
except FileExistsError:
    pass

RUN_DATA_FILE = os.path.join(RUN_DATA_DIR, "run_data.csv")
INFO_FILE = os.path.join(RUN_DATA_DIR, 'info.txt')

IMPLEMENTATION_LABEL = 'implementation'
ITER_LIMIT_LABEL = 'iteration limit'
PROCESSORS_AMOUNT_LABEL = 'processors amount'
RUN_TIME_LABEL = 'execution time (seconds)'
SPEEDUP_LABEL = 'speedup'
EFFICIENCY_LABEL = 'efficiency'

SEP = '----------------------------------------------------------------------------------------'
SHORT_SEP = '-----------------------------------------'

STATUS_COMMAND = 'sudo inxi -Ffmxxx -t c20 -z -! 31'
