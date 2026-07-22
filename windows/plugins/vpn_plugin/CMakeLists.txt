
cmake_minimum_required(VERSION 3.15)
project(vpn_plugin)

# Include Flutter engine headers
if(DEFINED FLUTTER_ENGINE_DIR)
    target_include_directories(vpn_plugin PRIVATE ${FLUTTER_ENGINE_DIR}/include)
else()
    message(WARNING "FLUTTER_ENGINE_DIR not defined, using default")
endif()

add_library(vpn_plugin SHARED vpn_plugin.cpp)
target_link_libraries(vpn_plugin PRIVATE flutter_engine)
target_link_libraries(vpn_plugin PRIVATE wininet advapi32 crypt32 shlwapi psapi iphlpapi)
