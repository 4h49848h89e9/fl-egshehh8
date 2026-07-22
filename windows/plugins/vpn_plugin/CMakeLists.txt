
cmake_minimum_required(VERSION 3.15)
project(vpn_plugin)

add_library(vpn_plugin SHARED vpn_plugin.cpp)
target_include_directories(vpn_plugin PRIVATE ${FLUTTER_ENGINE_DIR}/include)
target_link_libraries(vpn_plugin PRIVATE flutter_engine)
