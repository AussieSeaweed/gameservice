#!/usr/bin/env python
"""setuptools based setup script for gameframe."""
from setuptools import find_packages, setup

setup(
    name='gameframe',
    version='0.0.2',
    packages=find_packages(),
    license=open('LICENSE', 'r').read(),
    author='Juho Kim',
    author_email='juho-kim@outlook.com',
    description='A package for various game implementations on python',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AussieSeaweed/gameframe',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=['treys'],
)
