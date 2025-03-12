from setuptools import find_packages, setup

setup(
    name="security",
    version="0.1",
    packages=find_packages(),
    install_requires=["numpy", "urbasic", "matplotlib"],
    python_requires=">=3.10",
    author="6Figures",
    description="A package to allow robot security",

)