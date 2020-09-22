#pragma once

const int x_resolution = 1024;
const int y_resolution = 1024;
const int result_size = x_resolution * y_resolution;

void compute_mandelbrot_subset(int* result, int iter_limit,
                               int start = 0, int end = result_size);
