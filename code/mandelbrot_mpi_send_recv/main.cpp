#include "common/misc.h"
#include "common/now.h"
#include "common/compute_mandelbrot_subset.h"
#include "common/print_result.h"
#include <mpi.h>

void run(int iter_limit, int current_processor, int processors_amount, bool print) {
    int part_width = result_size / processors_amount;

    if (current_processor == 0) {
        int* result = new int[result_size];
        int* current = result;

        double first_measure = now();

        // distribute tasks
        int start, end = 0;
        for (int i = 1; i < processors_amount; i++) {
            start = end; end += part_width;
            int message[2] = {start, end};
            MPI_Send(message, 2, MPI_INT, i, 0, MPI_COMM_WORLD);
        }
        compute_mandelbrot_subset(current+end, iter_limit, end, result_size);
        // join pieces together
        for (int i = 1; i < processors_amount; i++) {
            MPI_Recv(current, part_width, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            current += part_width;
        }

        output_execution_time(now() - first_measure);

        if (print) print_result(result, iter_limit, "MPI_send_recv");
        delete[] result;
    }
    else {
        int message[2];
        MPI_Recv(message, 2, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        int* partial_result = new int[part_width];
        compute_mandelbrot_subset(partial_result, iter_limit, message[0], message[1]);
        MPI_Send(partial_result, part_width, MPI_INT, 0, 0, MPI_COMM_WORLD);
        delete[] partial_result;
    }
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
