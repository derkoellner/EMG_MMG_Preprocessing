import os
import subprocess
from setuptools import setup, find_packages
from setuptools.command.build_ext import build_ext as _build_ext

class BuildExtAndVendor(_build_ext):
    """first runs `make install` on vendor/pyctf."""
    def run(self):
        vendor_dir = os.path.join(os.path.dirname(__file__), "vendor", "pyctf")
        subprocess.check_call(["make", "install"], cwd=vendor_dir)
        super().run()

setup(
    cmdclass={
        "build_ext": BuildExtAndVendor,
    },
)