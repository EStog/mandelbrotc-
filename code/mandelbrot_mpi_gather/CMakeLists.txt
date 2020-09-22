cmake_minimum_required(VERSION 3.0)

project(mandelbrot_mpi_gather)

# sets the required compilation and linking flags of MPI
SET(CMAKE_CXX_COMPILE_FLAGS "-pthread")
SET(CMAKE_CXX_LINK_FLAGS "-pthread -L/usr/lib64 -llammpio -llammpi++ -llamf77mpi -lmpi -llam -lutil -ldl")

add_executable(mandelbrot_mpi_gather
    common/misc.cpp
    common/now.cpp
    common/compute_mandelbrot_subset.cpp
    common/print_result.cpp
    main.cpp
)


install(TARGETS mandelbrot_mpi_gather RUNTIME DESTINATION bin)
