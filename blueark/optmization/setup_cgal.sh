# This script sets up CGAL, enabling some nice features:
# - verification with valgrind
# - nice debugging with gbd (because of debug mode and optimization level O0)
# - all features from helpers.mk


# cleanup
rm -rf CMake* cmake* main Makefile
# create cmake script
rm -rf build 
mkdir build

cgal_create_cmake_script
cd build/
# enable c++11 features
echo 'set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")' >> CMakeLists.txt
# disable rounding math check: otherwise valgrind does not work
# lecho 'set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DCGAL_DISABLE_ROUNDING_MATH_CHECK")' >> CMakeLists.txt
# disable optimizations
echo 'set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")' >> CMakeLists.txt
# cmake with debugging enabled
<<<<<<< HEAD
cmake .
cmake -DCMAKE_BUILD_TYPE=Debug .
=======

cmake ..
cmake -DCMAKE_BUILD_TYPE=Release ..
cd ..
>>>>>>> representation
# append utils to Makefile
