import os
import warnings
import onnx
from tvm import relay
from tvm.relay.backend.contrib import tidl
from dlr import DLRModel
from .base_rt_session import BaseRTSession
from ..import utils


class TVMDLRSession(BaseRTSession):
    def __init__(self, session_name='tvm-dlr', **kwargs):
        super().__init__(session_name=session_name, **kwargs)
        self._set_default_options()
        self.interpreter = None
        self.interpreter_folder = os.path.join(os.environ['TIDL_BASE_PATH'], 'ti_dl/test/tvm-dlr')

    def import_model(self, calib_data):
        super().import_model(calib_data)
        os.chdir(self.interpreter_folder)

        model_path = self.kwargs['model_path']
        onnx_model = onnx.load(model_path)

        if self.kwargs['input_shape'] is None:
            self.kwargs['input_shape'] = self._get_input_shape(onnx_model)
        #
        input_shape = self.kwargs['input_shape']
        input_keys = list(input_shape.keys())

        tvm_model, params = relay.frontend.from_onnx(onnx_model, shape=input_shape)

        calib_list = []
        for c_data in calib_data:
            c_data = utils.as_tuple(c_data)
            c_dict = {d_name:d for d_name, d in zip(input_keys,c_data)}
            calib_list.append(c_dict)

        build_target = 'llvm'
        cross_cc_args = {}

        # Create the TIDL compiler with appropriate parameters
        compiler = tidl.TIDLCompiler(
            platform=self.kwargs['platform'],
            version=self.kwargs['version'],
            num_tidl_subgraphs=self.kwargs['num_tidl_subgraphs'],
            data_layout=self.kwargs['data_layout'],
            artifacts_folder=self.kwargs['artifacts_folder'],
            tidl_tools_path=os.path.join(os.environ['TIDL_BASE_PATH'], 'tidl_tools'),
            tidl_tensor_bits=self.kwargs['tidl_tensor_bits'],
            tidl_calibration_options=self.kwargs['tidl_calibration_options'])

        # partition the graph into TIDL operations and TVM operations
        tvm_model, status = compiler.enable(tvm_model, params, calib_list)

        # build the relay module into deployables
        with tidl.build_config(tidl_compiler=compiler):
            graph, lib, params = relay.build_module.build(tvm_model, target=build_target, params=params)

        # remove nodes / params not needed for inference
        tidl.remove_tidl_params(params)

        # save the deployables
        path_lib = os.path.join(self.kwargs['artifacts_folder'], 'deploy_lib.so')
        path_graph = os.path.join(self.kwargs['artifacts_folder'], 'deploy_graph.json')
        path_params = os.path.join(self.kwargs['artifacts_folder'], 'deploy_params.params')
        lib.export_library(path_lib, **cross_cc_args)
        with open(path_graph, "w") as fo:
            fo.write(graph)
        #
        with open(path_params, "wb") as fo:
            fo.write(relay.save_param_dict(params))
        #
        os.chdir(self.cwd)

    def start_infer(self):
        super().start_infer()
        # create inference model
        os.chdir(self.interpreter_folder)
        self.interpreter = DLRModel(self.kwargs['artifacts_folder'], 'cpu')
        os.chdir(self.cwd)
        self.import_done = True

    def infer_frame(self, input):
        if self.kwargs['input_shape'] is None:
            model_path = self.kwargs['model_path']
            onnx_model = onnx.load(model_path)
            self.kwargs['input_shape'] = self._get_input_shape(onnx_model)
        #
        super().infer_frame(input)
        input_shape = self.kwargs['input_shape']
        input_keys = list(input_shape.keys())
        in_data = utils.as_tuple(input)
        input_dict = {d_name:d for d_name, d in zip(input_keys,in_data)}
        output = self.interpreter.run(input_dict)
        return output

    def _set_default_options(self):
        # calibration options
        self.kwargs['data_layout'] = self.kwargs.get('data_layout', 'NCHW')
        self.kwargs["tidl_calibration_options"] = self.kwargs.get("tidl_calibration_options", {})

    def _get_input_shape(self, onnx_model):
        input_shape = {}
        num_inputs = self.kwargs['num_inputs']
        for input_idx in range(num_inputs):
            input_i = onnx_model.graph.input[input_idx]
            name = input_i.name
            shape = [dim.dim_value for dim in input_i.type.tensor_type.shape.dim]
            input_shape.update({name:shape})
        #
        return input_shape

if __name__ == '__main__':
    tvm_model = TVMDLRSession()
