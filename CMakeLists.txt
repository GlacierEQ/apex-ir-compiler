cmake_minimum_required(VERSION 3.15)
project(apex-ir-compiler)

find_package(MLIR REQUIRED)
list(APPEND CMAKE_MODULE_PATH "${MLIR_CMAKE_DIR}")
include(AddMLIR)

include_directories(${MLIR_INCLUDE_DIRS})

add_mlir_dialect(ApexDialect apex)
add_mlir_pass(LowerApexToStandard)
add_mlir_pass(ChangeSetVerifier)
