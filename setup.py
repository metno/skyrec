try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name = "Skyrec",
    version = "0.0.1",
    packages = find_packages(),
    install_requires = [
        "pyzmq==15.2.0",
        "pandas==0.18.1",
    ]
)
