#!/usr/bin/env bash

#################################################################################
# Copyright (c) 2018-2022, Texas Instruments Incorporated - http://www.ti.com
# All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#################################################################################

_PWD=$(pwd)

# check python version
if [[ $(python3 --version | awk '{print $2}') != "3.10."* ]]; then
    echo "Please use python 3.10.x"
    exit 1
fi
sudo apt update
sudo apt -y install build-essential libssl-dev libffi-dev python3-dev python3.10-venv
if [[ ! -d venv ]]; then python3 -m venv venv;fi
source $_PWD/venv/bin/activate

echo $_PWD 
#################################################################################
# internal or external repositories
# USE_INTERNAL_REPO=0

# set to 1 to enable other extra models
PLUGINS_ENABLE_EXTRA=0

#################################################################################
# if [[ ${USE_INTERNAL_REPO} -eq 0 ]]; then
#     SOURCE_LOCATION="https://github.com/TexasInstruments/"
#     FAST_CLONE_MODELZOO=""
# else
#     SOURCE_LOCATION="ssh://git@bitbucket.itg.ti.com/edgeai-algo/"
#     FAST_CLONE_MODELZOO="--single-branch"
# fi
# print
# echo "SOURCE_LOCATION="${SOURCE_LOCATION}

#################################################################################
# clone
# echo "cloning git repositories. this may take some time..."

# if [[ ! -d ../edgeai-benchmark ]]; then git clone --branch r9.0 ${SOURCE_LOCATION}edgeai-benchmark.git edgeai-benchmark; fi
# if [[ ! -d ../edgeai-mmdetection ]]; then git clone --branch r9.0 ${SOURCE_LOCATION}edgeai-mmdetection.git edgeai-mmdetection; fi
# if [[ ! -d ../edgeai-torchvision ]]; then git clone --branch r9.0 ${SOURCE_LOCATION}edgeai-torchvision.git edgeai-torchvision; fi
# if [[ ! -d ../edgeai-modelzoo ]]; then git clone ${FAST_CLONE_MODELZOO} --branch r9.0 ${SOURCE_LOCATION}edgeai-modelzoo.git edgeai-modelzoo; fi

# if [[ ${PLUGINS_ENABLE_EXTRA} -ne 0 ]]; then
#   if [[ ! -d ../edgeai-yolox ]]; then git clone --branch r9.0 ${SOURCE_LOCATION}edgeai-yolox.git edgeai-yolox; fi
#   sed -i s/'PLUGINS_ENABLE_EXTRA = False'/'PLUGINS_ENABLE_EXTRA = True'/g ./edgeai_modelmaker/ai_modules/vision/constants.py
# fi

# echo "cloning done."

#################################################################################
# upgrade pip
pip install --no-input --upgrade pip setuptools
pip install --no-input --upgrade wheel cython numpy==1.23.0

#################################################################################
echo "preparing environment..."
# for setup.py develop mode to work inside docker environment, this is required
git config --global --add safe.directory $(pwd)

echo "installing repositories..."

echo "installing: edgeai-torchvision"
cd $_PWD/edgeai-torchvision
./setup.sh

echo "installing: edgeai-mmdetection"
cd $_PWD/edgeai-mmdetection
./setup.sh

if [[ ${PLUGINS_ENABLE_EXTRA} -ne 0 ]]; then
  echo "installing: edgeai-yolox"
  cd $_PWD/edgeai-yolox
  ./setup.sh
fi

# uninstall the onnxruntime was installed by setups above, so that the correct version can be installed.
pip uninstall --yes onnxruntime

echo "installing: edgeai-benchmark"
cd $_PWD/edgeai-benchmark
./setup_pc.sh r9.0

echo "installing edgeai-modelmaker"
cd $_PWD/edgeai-modelmaker
./setup.sh

# make sure that we are using pillow-simd (which is faster)
pip uninstall --yes pillow
pip install --no-input -U --force-reinstall pillow-simd

ls -d $_PWD/edgeai-*

# patch
pip install --upgrade mmcv_full==1.7.2 -f https://download.openmmlab.com/mmcv/dist/cu118/torch2.0/index.html
pybind11_DIR=$(pybind11-config --cmakedir) pip3 install --upgrade --no-input https://github.com/TexasInstruments/onnx/archive/tidl-j7.zip
# fix: no module named pkg_resources
pip install --upgrade setuptools==69.5.1
# fix: no module named mmdet
cd $_PWD/edgeai-mmdetection
python -m pip install -e .
# fix libnvrtc.so not found
cd $_PWD/venv/lib/python3.10/site-packages/torch/lib/ 
ln -s libnvrtc-*.so.11.2 libnvrtc.so

pip install --upgrade "protobuf==3.20.3"
cd $_PWD
echo "installation done."
