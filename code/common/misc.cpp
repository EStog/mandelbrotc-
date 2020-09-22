#include "misc.h"
#include <iostream>

using namespace std;

//process command arguments
void get_iter_limit(int argc, char **argv, int &iter_limit, bool &print) {
    try {
        switch (argc) {
            case 2:
                iter_limit = stoi(argv[--argc]);
                print = false;
                return;
            case 3:
                iter_limit = stoi(argv[--argc]);
                print = stoi(argv[--argc]);
                return;
            case 1:
                cout << endl;
                cout << "Pass at least one argument" << endl;
        }
    }
    catch (exception) {
        cout << endl;
        cout << "Wrong arguments" << endl;
    }
    cout << "Parameters syntax after program name: [<print>] <iter_limit>" << endl;
    cout << "<print>: Whether to print the set to a file or not. This must be somethig that can be converted to boolean" << endl;
    cout << "<iter_limit>: The iteration limit. This must be a positive integer" << endl;
    cout << endl;
    exit(1);
}

void output_execution_time(double time) {
    cout << time << endl;
}
