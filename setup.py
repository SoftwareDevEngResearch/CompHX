#!/usr/bin/env python3

try:
    from setuptools import setup, find_packages
    
except ImportError:
    from distutils.core import setup

setup(
    name='comp_hx',
    version='0.1.0',
    description='Analytical Heat Exchanger Solver',
    author='Tommy Moore',
    author_email='tommy.moore22@gmail.com',
    url='https://github.com/SoftwareDevEngResearch/CompHX',
    classifiers=[
        'License :: BSD License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    license='BSD-3-Clause',
    python_requires='>=3',
    zip_safe=False,
    packages=['comphx'],
    # or find automatically:
    package=find_packages(),
    package_dir={
        'comphx',
        },
    include_package_data=True,

#    # or you can specify explicitly:
#    package_data={
#        'compphys': ['assets/*.txt']
#        },
)