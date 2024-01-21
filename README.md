# Personal Project: Image Classification

This repository contains the files used in my personal project (IB), which was about image classification. Specifically, writing a classifier machine learning model to predict the "type" of object in an image.

You can replicate my image classifier by downloading the contents of this repository and performing the necessary installations on your device. To get the website working locally, you should install Anaconda and, from the Anaconda terminal, use the `exts-ml.yml` file (from the EPFL Extension School) to install the relevant machine learning libraries as well as Flask. Then, run `py api.py` and visit the URL that appears in the terminal.

The dataset used for training/testing is CIFAR-100. It is referenced in my report.

Description of the files:
- `api.py` = Python file that implements the backend functionality of the website.
- `models` folder contains a set of files that can be read by the Keras module in Python to replicate the effects of my models programmatically.
- `static` folder contains the frontend files of my website - HTML, CSS and JS as well as images.
- `The project.ipynb` is a Jupyter notebook that documents all of my code. Unfortunately, it got too big, so I started...
- `The project two.iypnb`, which is a Jupyter notebook that documents the latter stages of my project.
