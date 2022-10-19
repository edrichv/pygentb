#! /bin/bash

python3 -m venv env && \
source env/bin/activate && \
pip install --upgrade setuptools==57 && \
pip install -r requirements.txt
