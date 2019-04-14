#!/usr/bin/python3
from setuptools import setup, find_packages

setup(
    name='matrixcli',
    version='0.1',
    description='command line matrix client',
    long_description='for more info https://git.saadnpq.com/saad/matrixcli',
    long_description_content_type="text/plain",
    author='saadnpq',
    author_email='saad@saadnpq.com',
    url='https://git.saadnpq.com/saad/matrixcli',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Conferencing',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='chat matrix command line',
    data_files=[('/etc/matrixcli', ['config.py']),('/lib/systemd/user', ['matrixcli.service'])],
    packages=find_packages(),
    scripts=['matrixcli']
)
