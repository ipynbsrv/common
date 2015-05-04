import os
from setuptools import setup, find_packages

setup(
    name="ipynbsrv-common",
    description="Common package for various stuff shared across multiple ipynbsrv packages.",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['ipynbsrv']
)
