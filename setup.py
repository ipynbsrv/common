from setuptools import setup, find_packages

setup(
    name="coco-common",
    description="Common package for various stuff shared across multiple coco packages.",
    version="0.0.1",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['coco'],
    install_requires=[
        'coco-contract',
        'pathlib==1.0.1',
        'rsa==3.1.4'
    ],
)
