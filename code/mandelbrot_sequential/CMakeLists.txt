cmake_minimum_required(VERSION 3.0)

project(mandelbrot_sequential)

add_executable(mandelbrot_sequential
    common/misc.cpp
    common/now.cpp
    common/compute_mandelbrot_subset.cpp
    common/print_result.cpp
    main.cpp
)

install(TARGETS mandelbrot_sequential RUNTIME DESTINATION bin)
