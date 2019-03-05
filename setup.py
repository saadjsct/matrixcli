from setuptools import setup, find_packages

setup(
    name='matrixcli',
    version='0.1',
    description='command line matrix client',
    long_description='README.md',
    long_description_content_type="text/markdown",
    author='saadnpq',
    author_email='saad@saadnpq.com',
    url='',
    packages=find_packages(),
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Communications :: Chat',
        'Topic :: Communications :: Conferencing',
    ],
    keywords='chat matrix matrix.org command line',
    install_requires=[
        'requests',
        'urllib3',
    ],
)
