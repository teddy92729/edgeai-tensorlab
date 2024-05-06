# Copyright (c) 2018-2021, Texas Instruments
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

from edgeai_benchmark import constants, utils, datasets, preprocess, sessions, postprocess, metrics


def get_configs(settings, work_dir):
    # get the sessions types to use for each model type
    onnx_session_type = settings.get_session_type(constants.MODEL_TYPE_ONNX)

    preproc_transforms = preprocess.PreProcessTransforms(settings)
    postproc_transforms = postprocess.PostProcessTransforms(settings)

    # configs for each model pipeline
    common_cfg = {
        'task_type': 'detection_3d',
        'dataset_category': datasets.DATASET_CATEGORY_KITTI_LIDAR_DET,
        'calibration_dataset': settings.dataset_cache['kitti_lidar_det']['calibration_dataset'],
        'input_dataset': settings.dataset_cache['kitti_lidar_det']['input_dataset'],
        'postprocess': None
    }

    # to define the names of first and last layer for 16 bit conversion
    first_last_layer_3dod_7100 = ''

    pipeline_configs = {
        #################################################################
        #       ONNX MODELS
        ################# onnx models ###############################
        '3dod-7100':utils.dict_update(common_cfg,
            preprocess=preproc_transforms.get_transform_lidar_base(),
            session=onnx_session_type(**sessions.get_nomeanscale_session_cfg(settings, work_dir=work_dir),
                runtime_options=settings.runtime_options_onnx_qat(det_options=True,
                    ext_options={'object_detection:meta_arch_type': 7,
                     'object_detection:meta_layers_names_list':f'{settings.models_path}/vision/detection_3d/kitti/mmdet3d/lidar_point_pillars_10k_496x432.prototxt',
                     "advanced_options:add_data_convert_ops" : 0,
                     'advanced_options:output_feature_16bit_names_list': first_last_layer_3dod_7100}),
                model_path=f'{settings.models_path}/vision/detection_3d/kitti/mmdet3d/lidar_point_pillars_10k_496x432_qat-p2.onnx'),
            postprocess=postproc_transforms.get_transform_lidar_base(),
            metric=dict(label_offset_pred=None),
            model_info=dict(metric_reference={'accuracy_ap_3d_moderate%':76.50}, model_shortlist=20)
        ),
        '3dod-7110':utils.dict_update(common_cfg,
            preprocess=preproc_transforms.get_transform_lidar_base(),
            session=onnx_session_type(**sessions.get_nomeanscale_session_cfg(settings, work_dir=work_dir),
                runtime_options=settings.runtime_options_onnx_qat(det_options=True,
                    ext_options={'object_detection:meta_arch_type': 7,
                     'object_detection:meta_layers_names_list':f'{settings.models_path}/vision/detection_3d/kitti/mmdet3d/lidar_point_pillars_10k_496x432_3class.prototxt',
                     "advanced_options:add_data_convert_ops" : 0,
                     'advanced_options:output_feature_16bit_names_list': first_last_layer_3dod_7100}),
                model_path=f'{settings.models_path}/vision/detection_3d/kitti/mmdet3d/lidar_point_pillars_10k_496x432_3class_qat-p2.onnx'),
            postprocess=postproc_transforms.get_transform_lidar_base(),
            metric=dict(label_offset_pred=None),
            model_info=dict(metric_reference={'accuracy_ap_3d_moderate%':76.50}, model_shortlist=20)
        )
    }

    return pipeline_configs