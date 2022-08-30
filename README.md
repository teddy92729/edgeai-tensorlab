# EdgeAI-MMDetection3D



This repository is an extension of the popular [mmdetection3d](https://github.com/open-mmlab/mmdetection3d) open source repository for 3d object detection. While mmdetection3d focuses on a wide variety of models, typically at high complexity, we focus on models that are optimized for speed and accuracy so that they run efficiently on embedded devices. For this purpose, we have added a set of embedded friendly model configurations and scripts.

If the accuracy degradation with Post Training Quantization (PTQ) is higher than expected, for that pupose this repository provides instructions and functionality to do Quantization Aware Training (QAT).

<hr>


## Release Notes
See notes about recent changes/updates in this repository in [release notes](./docs/det3d_release_notes.md)


## Installation
Follow installation steps of [edgeai-torchvision](https://github.com/TexasInstruments/edgeai-torchvision) to install edgeai-torchvision. In same environment install [mmdetection3d](README_mmdet3d.md) by skipping pytorch and CUDA installtion step mentioned in the [mmdetection3d Installation Guide](./docs/en/getting_started.md#installation). As pytorch and CUDA must have been installed as part of edgeai-torchvision installation. It has been tested for torch==1.10.0 and cuda = 11.3. edgeai-torchvision installation is required for QAT training only.

If QAT is not needed then edgeai-torchvision installation can be skipped and complete steps of mmdetection3d installation has to be followed. 

## Get Started
Please see [Usage](./docs/det3d_usage.md) for training and testing with this repository.


## 3D Object Detection Model Zoo
Complexity and Accuracy report of several trained models is available at the [3D Detection Model Zoo](./docs/det3d_modelzoo.md) 


## Quantization
This tutorial explains more about quantization and how to do [Quantization Aware Training (QAT)](./docs/det3d_quantization.md) of detection models.


## ONNX & Prototxt Export
**Export of ONNX model (.onnx) and additional meta information (.prototxt)** is supported. The .prototxt contains meta information specified by **TIDL** for object detectors. 

The export of meta information is now supported for **pointPillars** detectors.

For more information please see [Usage](./docs/det3d_usage.md)


## Advanced documentation
Kindly take time to read through the documentation of the original [mmdetection3d](README_mmdet3d.md) before attempting to use extensions added to this repository.


 
## Acknowledgement

This is an open source project that is contributed by researchers and engineers from various colleges and companies. We appreciate all the contributors who implement their methods or add new features, as well as users who give valuable feedbacks.

We wish that the toolbox and benchmark could serve the growing research community by providing a flexible toolkit to train existing detectors and also to develop their own new detectors.


## License

Please see [LICENSE](./LICENSE) file of this repository.


## Model deployment

Now MMDeploy has supported some MMDetection3D model deployment. Please refer to [model_deployment.md](docs/en/tutorials/model_deployment.md) for more details.

## Citation

This package/toolbox is an extension of mmdetection3d (https://github.com/open-mmlab/mmdetection3d). If you use this repository or benchmark in your research or work, please cite the following:

```
@article{EdgeAI-MMDetection3D,
  title   = {{EdgeAI-MMDetection3D}: An Extension To Open MMLab Detection Toolbox and Benchmark},
  author  = {Texas Instruments EdgeAI Development Team, edgeai-devkit@list.ti.com},
  journal = {https://github.com/TexasInstruments/edgeai},
  year={2022}
}
```

```
@misc{mmdet3d2020,
    title={{MMDetection3D: OpenMMLab} next-generation platform for general {3D} object detection},
    author={MMDetection3D Contributors},
    howpublished = {\url{https://github.com/open-mmlab/mmdetection3d}},
    year={2020}
}
```

## References
[1] MMDetection3d: https://github.com/open-mmlab/mmdetection3d