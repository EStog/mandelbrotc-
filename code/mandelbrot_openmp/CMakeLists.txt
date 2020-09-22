cmake_minimum_required(VERSION 3.0)

project(mandelbrot_openmp)

INCLUDE(FindOpenMP)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
SET(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")

add_executable(mandelbrot_openmp
    common/misc.cpp
    common/now.cpp
    common/compute_mandelbrot_subset.cpp
    common/print_result.cpp
    main.cpp
)

install(TARGETS mandelbrot_openmp RUNTIME DESTINATION bin)
