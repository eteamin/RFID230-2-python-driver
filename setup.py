# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


install_requires = [
    "pySerial"
]

setup(
    name='rfid230-2_reader',
    version='0.1',
    description='python driver for rfid230-2_reader',
    author='eteamin',
    author_email='aminetesamian1371@gmail.com',
    url='https://github.com/eteamin/RFID230-2-python-driver',
    packages=find_packages(),
    install_requires=install_requires,
)
