import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gameservice",
    version="2.0.1",
    author="Juho Kim",
    author_email="juho-kim@outlook.com",
    description="A package for game services on python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AussieSeaweed/gameservice",
    packages=setuptools.find_packages(exclude=("tests",)),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["treys"],
)
