#!/usr/bin/env bash
python ./setup.py install || exit 1
cd ./matrix-python-sdk
python ./setup.py install
cd ..
