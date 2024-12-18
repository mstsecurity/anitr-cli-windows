cmake_minimum_required(VERSION 3.12)

project(anitr-cli VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native -flto -funroll-loops -ftree-vectorize")

set(SOURCES
    modules/anitr_fetch.cpp
    anitr-cli.cpp
)

add_executable(anitr-cli ${SOURCES})

target_link_libraries(anitr-cli PRIVATE curl)

