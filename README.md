# EdgeAI-TorchVision 

**Note: This repository is under development. Please revisit after a few days.** 

Develop Embedded Friendly Deep Neural Network Models in ![PyTorch](./docs/source/_static/img/pytorch-logo-flame.png) **PyTorch**

This is an extension of the popular github repository [pytorch/vision](https://github.com/pytorch/vision) that implements PyTorch based datasets, model architectures, and common image transformations for computer vision.

The scripts in this repository requires torchvision to be installed using this repository - the standard torchvision will not support all the features in this repository. Please install our torchvision extension using the instructions below.

<hr>

## Installation Instructions
These instructions are for installation on **Ubuntu 18.04**. 

Install Miniconda with Python 3.7 (higher version might also work) from https://docs.conda.io/en/latest/miniconda.html <br>

After the installation, make sure that your python is indeed Miniconda Python 3.7 or higher by typing:<br>
```
python --version
```

Clone this repository into your local folder

Execute the following shell script to install the dependencies:<br>
```
./setup.sh
```

<hr>

## Categories of Models and Scripts
We have two three categories of models in this repository:

- Models and scripts that can be used to train a Lite version of the original torchvision models. These models will carry a keyword called "lite". The training scripts for these are in the folder [references](./references) have been altered to train these "lite" models.
- Models and scripts that we have implemented and are best suited for our devices. The training scripts for these are in the folder [references/edgeailite](./references/edgeailite) - and they invoke "our extensions to torchvision". The models trained using these scripts will carry a keyword "edgeailite".
- Then there are the original torchvision models, without any change. It is best that the original torchvision repository be used for training those models.

<hr>

## Our Extensions to Torchvision
We have added extensions to Torchvision that allows training of low complexity, embedded friendly Deep Neural Network models. 

Scripts provided for training low complexity DNN models for tasks such as:

- Image Classification
- Semantic Segmentation
- Motion Segmentation
- Depth Estimation
- Multi-Task Estimation
- And more...

Tools and scripts for **Quantization Aware Training (QAT)** that is best suited for our devices are also provided. 

**[See Our Extensions to TorchVision](README_Pixel2Pixel.md)**

<hr>

## Original Torchvision documentation
**[See the Original TorchVision documentation](README.rst)**
![](https://static.pepy.tech/badge/torchvision) ![](https://img.shields.io/badge/dynamic/json.svg?label=docs&url=https%3A%2F%2Fpypi.org%2Fpypi%2Ftorchvision%2Fjson&query=%24.info.version&colorB=brightgreen&prefix=v)

<hr>
