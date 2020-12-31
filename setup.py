import setuptools

setuptools.setup(
    name='gameframe',
    version='0.0.2',
    author='Juho Kim',
    author_email='juho-kim@outlook.com',
    description='A package for various game implementations on python',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AussieSeaweed/gameframe',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    install_requires=['treys'],
)
