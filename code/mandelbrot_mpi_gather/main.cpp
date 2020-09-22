#include "common/misc.h"
#include "common/now.h"
#include "common/compute_mandelbrot_subset.h"
#include "common/print_result.h"
#include <mpi.h>

void run(int iter_limit, int current_processor, int processors_amount, bool print) {
    int* result;
    int part_width = result_size / processors_amount;
    int start = current_processor * part_width;
    int* partial_result = new int[part_width];

    double first_measure;
    if (current_processor == 0 ) {
        result = new int[result_size];

        first_measure = now();
    }

    compute_mandelbrot_subset(partial_result, iter_limit, start, start+part_width);
    MPI_Gather(partial_result, part_width, MPI_INT, result, part_width, MPI_INT, 0, MPI_COMM_WORLD);

    if (current_processor == 0) {
        output_execution_time(now() - first_measure);

        if (print) print_result(result, iter_limit, "MPI_gather");
        delete[] result;
    }

    delete[] partial_result;
}

int main(int argc, char **argv) {
    int iter_limit; bool print;
    get_iter_limit(argc, argv, iter_limit, print);

    int current_processor, processors_amount;
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &current_processor);
    MPI_Comm_size(MPI_COMM_WORLD, &processors_amount);

    run(iter_limit, current_processor, processors_amount, print);

    MPI_Finalize();
    return 0;
}
