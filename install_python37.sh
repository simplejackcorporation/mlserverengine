#!/bin/bash
# Setup env for Python 3.7 for Google Cloud (Ubuntu)
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt install python3.7 python3.7-dev python3.7-venv
wget https://bootstrap.pypa.io/get-pip.py
sudo python3.7 get-pip.py
sudo apt install libpython3.7-dev
