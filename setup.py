from setuptools import setup, find_packages
setup(
    name = "Skyrec",
    version = "0.0.1",
    packages = find_packages(),
    install_requires = [
        "pyzmq==15.2.0",
    ]
)
