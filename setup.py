#!/usr/bin/env python3

try:
    from setuptools import setup, find_packages
    
except ImportError:
    from distutils.core import setup

setup(
    name='CompHX',
    version='0.1.0',
    description='Analytical Heat Exchanger Solver',
    author='Tommy Moore',
    author_email='tommy.moore22@gmail.com',
    url='https://github.com/SoftwareDevEngResearch/CompHX',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
#   license='MIT',
    python_requires='>=3',
    zip_safe=False,
#    packages=['comphx'],
    # or find automatically:
    package=find_packages(),
#    package_dir={
#        'comphx',
#        },
#    include_package_data=True,

#    # or you can specify explicitly:
#    package_data={
#        'compphys': ['assets/*.txt']
#        },
)
