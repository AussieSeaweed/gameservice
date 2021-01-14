from setuptools import find_packages, setup

setup(
    name='gameframe',
    version='0.0.1.dev1',
    author='Juho Kim',
    author_email='juho-kim@outlook.com',
    description='A package for various game implementations on python',
    long_description=open('README.rst', 'r').read(),
    long_description_content_type='text/x-rst',
    url='https://github.com/AussieSeaweed/gameframe',
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
    install_requires=['treys'],
)
