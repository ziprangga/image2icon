import os
import subprocess
from setuptools import setup
from setuptools.command.build_ext import build_ext


class CMakeBuild(build_ext):
    def run(self):
        if subprocess.call(["cmake", "--version"]) != 0:
            raise RuntimeError("CMake is required but not installed.")

        build_dir = os.path.join(self.build_temp, "build")
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        cmake_args = [
            "cmake",
            os.path.dirname(__file__),
            "-DCMAKE_BUILD_TYPE=Release",
        ]
        subprocess.check_call(cmake_args, cwd=build_dir)

        subprocess.check_call(
            ["cmake", "--build", ".", "--config", "Release"], cwd=build_dir
        )

        super().run()


setup(
    name="image2icon",
    version="0.1",
    packages=["pysrc"],
    cmdclass={"build_ext": CMakeBuild},
    install_requires=["customtkinter", "pillow", "pyinstaller"],
    author="ziprangga",
    description="Converter utility for image to icns and ico",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ziprangga/image2icon",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13.0",
)
