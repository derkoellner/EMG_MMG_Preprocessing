import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext

class BuildExtAndVendor(_build_ext):
    """first runs `make install` on vendor/pyctf."""
    def run(self):
        vendor_dir = os.path.join(os.path.dirname(__file__), "vendor", "pyctf")
        # 1) invoke the NIH Makefile to compile/install C code
        subprocess.check_call(["make", "install"], cwd=vendor_dir)
        # 2) let setuptools do the rest (including building any extensions)
        super().run()

setup(
    name="emg-mmg-preprocessing-pipeline",
    version="0.1.0",
    description="EMG and MMG data loading and preprocessing pipeline",
    packages=find_packages(include=["preprocessing_pipeline", "pyctf", "pyctf.*"]),
    python_requires=">=3.10",
    install_requires=[
        "numpy>=2.2.6",
        "scipy>=1.15.3",
        "matplotlib>=3.10.3",
    ],
    cmdclass={
        "build_ext": BuildExtAndVendor,
    },
    package_dir={
        "preprocessing_pipeline": "preprocessing_pipeline",
        "pyctf": "vendor/pyctf/pyctf",
    },
    include_package_data=True,
    zip_safe=False,
)