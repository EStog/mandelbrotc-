#include "common/misc.h"
#include "common/now.h"
#include "common/compute_mandelbrot_subset.h"
#include "common/print_result.h"


int main(int argc, char **argv) {
    int iter_limit; bool print;
    get_iter_limit(argc, argv, iter_limit, print);

    int* result = new int[result_size];

    double firt_measure = now();

    compute_mandelbrot_subset(result, iter_limit);

    output_execution_time(now() - firt_measure);

    if (print) print_result(result, iter_limit, "Sequential");

    delete[] result;
    return 0;
}
