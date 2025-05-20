import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py

class CustomBuild(_build_py):
    def run(self):
        # Build NIH pyctf extension via its Makefile
        vendor_dir = os.path.join("vendor", "pyctf")
        subprocess.check_call(["make", "install"], cwd=vendor_dir)

        super().run()

setup(
    name="emg-mmg-preprocessing",
    version="0.1.0",
    packages=find_packages(include=[
        "preprocessing_pipeline",
        "pyctf",]),
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        "build_py": CustomBuild,
    },
    package_dir={
        "preprocessing_pipeline": "preprocessing_pipeline",
        "pyctf": "vendor/pyctf/pyctf"
    },
)
