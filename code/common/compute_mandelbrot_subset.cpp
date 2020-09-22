#include "compute_mandelbrot_subset.h"
#include <complex>

using namespace std;

const double x_begin = -2.0, x_end = 0.6;
const double y_begin = -1.2, y_end = 1.2;
const double x_step = (x_end-x_begin) / (x_resolution-1);
const double y_step = (y_end-y_begin) / (y_resolution-1);

void compute_mandelbrot_subset(int* result, int iter_limit, int start, int end) {
    int i, j;
    complex<double> c, z;

    #pragma omp parallel shared(result, iter_limit, start, end) private(i, j, c, z)
    #pragma omp for schedule(runtime)
    for (i = start; i < end; i++) {
        c = complex<double>(
                x_begin + (i % x_resolution) * x_step,
                y_begin + (i / x_resolution) * y_step
        );
        z = 0; j = 0;
        while (norm(z) <= 4 && j < iter_limit) {
            z = z*z + c;
            j++;
        }
        result[i-start] = j;
    }
}
