from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Music_Composer",
    version="0.1",
    author="Naveen Narasimhappa",
    packages=find_packages(),
    install_requires = requirements,
)