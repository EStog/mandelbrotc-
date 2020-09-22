#include "now.h"
#include <ctime>
#include <cstdlib>

double now() {
    struct timespec tp;
    if (clock_gettime(CLOCK_MONOTONIC_RAW, &tp) != 0)
        exit(1);
    return tp.tv_sec + tp.tv_nsec / (double)1000000000;
}
