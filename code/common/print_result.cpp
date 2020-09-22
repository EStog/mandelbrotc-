#include "print_result.h"
#include "compute_mandelbrot_subset.h"
#include <fstream>
#include <iostream>

using namespace std;

const unsigned short max_color = 65535;
const string mandelbrot_file_name ="../../../images/mandelbrot";

// Used to store mandelbrot set into an image file.
void print_result(int* result, int iter_limit, const char* name) {
    ofstream file;
    file.open(mandelbrot_file_name);
    file << "P3" << endl;
    file << x_resolution << " " << y_resolution << endl;
    file << max_color << endl;
    for (int i = 1; i <= y_resolution; i++) {
        for (int j = 0; j < x_resolution; j++) {
            int k = result[(i - 1) * x_resolution + j];
            file << " ";
            if (k == iter_limit)
                file << 0 << " " << 0 << " " << 0;
            else {
                unsigned short x = k * max_color / iter_limit;
                file << x / 4 << " ";
                file << x / 2 + max_color / 2 << " ";
                file << x;
            }
            file << " ";
        }
        file << endl;
    }
    file.close();

    string command = "pnmtojpeg -quality=100 -smooth=100 -optimize ./"+mandelbrot_file_name+" > "+mandelbrot_file_name+"_limit="+to_string(iter_limit)+"_"+name+".jpeg";

    if (system(command.c_str()) != 0)
        exit(1);

    system(("rm "+mandelbrot_file_name).c_str());
}
