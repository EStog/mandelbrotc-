#include "common/misc.h"
#include "common/now.h"
#include "common/compute_mandelbrot_subset.h"
#include "common/print_result.h"
#include <omp.h>

int main(int argc, char **argv) {
    int iter_limit; bool print;
    get_iter_limit(argc, argv, iter_limit, print);

    int* result = new int[result_size];

    double firt_measure = now();

    compute_mandelbrot_subset(result, iter_limit);

    output_execution_time(now() - firt_measure);

    if (print) print_result(result, iter_limit, "OpenMP");

    delete[] result;
    return 0;
}

//OMP_NUM_THREADS=<threads amount> OMP_SCHEDULE=[static, dynamic or guided] ./mandelbrot_openmp
