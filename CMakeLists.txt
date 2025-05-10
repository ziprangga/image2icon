cmake_minimum_required(VERSION 4.0.1) 

# Set project name
project(image2icon)

# Define your Rust library name & build mode
set(RUST_LIB_NAME image2icon)

# Set the default build mode (Release or Debug) using CMake's CMAKE_BUILD_TYPE
if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
endif()

# Set custom output directory for cargo builds
set(RUST_OUTPUT_DIR ${CMAKE_BINARY_DIR}/rust_target)

# Detect current platform
if (APPLE)
    set(SYSTEM "macos")
    set(TARGET_X86 x86_64-apple-darwin)
    set(TARGET_ARM aarch64-apple-darwin)
    set(LIB_EXTENSION ".dylib")
elseif (UNIX)
    set(SYSTEM "linux")
    set(TARGET_X86 x86_64-unknown-linux-gnu)
    set(TARGET_ARM aarch64-unknown-linux-gnu)
    set(LIB_EXTENSION ".so")
elseif (WIN32)
    set(SYSTEM "windows")
    set(TARGET_X86 x86_64-pc-windows-msvc)
    set(TARGET_ARM aarch64-pc-windows-msvc)
    set(LIB_EXTENSION ".dll")
else()
    message(FATAL_ERROR "Unsupported platform!")
endif()

# Set the CARGO_BUILD_MODE based on CMAKE_BUILD_TYPE (Release or Debug)
if (CMAKE_BUILD_TYPE STREQUAL "Release")
    set(CARGO_BUILD_MODE "--release")
    set(TARGET_BUILD release)
else()
    set(CARGO_BUILD_MODE "")
    set(TARGET_BUILD debug)
endif()

# Define library paths using RUST_OUTPUT_DIR
set(LIB_X86 ${RUST_OUTPUT_DIR}/${TARGET_BUILD}/x86_64/lib${RUST_LIB_NAME}${LIB_EXTENSION})
set(LIB_ARM ${RUST_OUTPUT_DIR}/${TARGET_BUILD}/aarch64/lib${RUST_LIB_NAME}${LIB_EXTENSION})
set(LIB_UNIVERSAL ${RUST_OUTPUT_DIR}/${TARGET_BUILD}/universal2/lib${RUST_LIB_NAME}${LIB_EXTENSION})

# Custom target to build Rust library for x86_64
add_custom_command(
    OUTPUT ${LIB_X86}
    COMMAND CARGO_TARGET_DIR=${RUST_OUTPUT_DIR} cargo build ${CARGO_BUILD_MODE} --target=${TARGET_X86}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${RUST_OUTPUT_DIR}/${TARGET_BUILD}/x86_64
    COMMAND ${CMAKE_COMMAND} -E copy
        ${RUST_OUTPUT_DIR}/${TARGET_X86}/${TARGET_BUILD}/lib${RUST_LIB_NAME}${LIB_EXTENSION}
        ${LIB_X86}
    COMMENT "Building Rust library for x86_64"
)

# Custom target to build Rust library for aarch64
add_custom_command(
    OUTPUT ${LIB_ARM}
    COMMAND CARGO_TARGET_DIR=${RUST_OUTPUT_DIR} cargo build ${CARGO_BUILD_MODE} --target=${TARGET_ARM}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${RUST_OUTPUT_DIR}/${TARGET_BUILD}/aarch64
    COMMAND ${CMAKE_COMMAND} -E copy
        ${RUST_OUTPUT_DIR}/${TARGET_ARM}/${TARGET_BUILD}/lib${RUST_LIB_NAME}${LIB_EXTENSION}
        ${LIB_ARM}
    COMMENT "Building Rust library for aarch64"
)

# Create universal2 binary using lipo (Only for macOS)
if (APPLE)
    add_custom_target(
        universal2
        DEPENDS ${LIB_X86} ${LIB_ARM}
        COMMAND ${CMAKE_COMMAND} -E make_directory ${RUST_OUTPUT_DIR}/${TARGET_BUILD}/universal2
        COMMAND lipo -create ${LIB_X86} ${LIB_ARM} -output ${LIB_UNIVERSAL}
        COMMENT "Creating universal2 library for macOS"
    )
endif()

# Set the path to your PyInstaller spec file
set(PYINSTALLER_SPEC ${CMAKE_SOURCE_DIR}/main.spec)

# Define the output directory for PyInstaller
set(PYINSTALLER_OUTPUT_DIR ${CMAKE_BINARY_DIR}/pyinstaller_output)

# Define a custom target for PyInstaller, without the 'ALL' argument
add_custom_target(pyinstaller
    DEPENDS universal2
    COMMAND ${CMAKE_COMMAND} -E make_directory ${PYINSTALLER_OUTPUT_DIR}
    COMMAND pyinstaller ${PYINSTALLER_SPEC} --distpath ${PYINSTALLER_OUTPUT_DIR}/dist --workpath ${PYINSTALLER_OUTPUT_DIR}/build
    COMMENT "Building Python GUI using PyInstaller and bundling Rust library"
)

# Optional clean target
add_custom_target(
    clean-all
    COMMAND rm -rf ${RUST_OUTPUT_DIR}
    COMMAND rm -rf ${CMAKE_BINARY_DIR}/pyinstaller_output
    COMMAND rm -f ${ENV_FILE}
    COMMENT "Cleaning build artifacts"
)
