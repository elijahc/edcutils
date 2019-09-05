from setuptools import setup, find_packages  # Always prefer setuptools over distutils
from codecs import open
from os import path
import subprocess
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))

with open(path.join(here,'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name = 'edcutils',

        version='0.0.1',
        packages = ['edcutils','edcutils.utils','edcutils.datasets'],
        description = 'edc personal utils',
        author = 'Elijah C',
        author_email = 'elijah.christensen@ucdenver.edu',
        url = 'https://github.com/elijahc/edcutils',
        classifiers = [],
)
