#!/usr/bin/python3

from setuptools import setup, find_packages
import os

HOME = os.getenv('HOME')

setup(
    name='matrixcli',
    version='0.1',
    description='command line matrix client',
    long_description='for more info https://git.saadnpq.com/saad/matrixcli',
    long_description_content_type="text/plain",
    author='saadnpq',
    author_email='saad@saadnpq.com',
    url='https://git.saadnpq.com/saad/matrixcli',
    license='Apache License, Version 2.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Conferencing',
        'Operating System :: POSIX :: Linux',
 
    ],
    keywords='chat matrix command line',
    install_requires=['matrix_client',],
    data_files=[(HOME+'/.config/matrixcli', ['config.py'])],
    scripts=['matrixcli']
)
