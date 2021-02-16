from setuptools import find_packages, setup

with open('README.rst', 'r') as long_description_file:
    long_description = long_description_file.read()

setup(
    name='gameframe',
    version='0.0.2.dev10',
    author='Juho Kim',
    author_email='juho-kim@outlook.com',
    description='A Python package for various game implementations',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/AussieSeaweed/gameframe',
    packages=find_packages(),
    package_data={'gameframe': ['py.typed']},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.9',
    install_requires=['pokertools'],
)
