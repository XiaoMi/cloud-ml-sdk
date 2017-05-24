#!/usr/bin/env python

# Copyright 2017 Xiaomi, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from grpc.beta import implementations
import json
import numpy as np
import os
import tensorflow as tf
from tensorflow.python.framework import tensor_util

import predict_pb2
import prediction_service_pb2

tf.app.flags.DEFINE_string("server", "localhost:9000",
                           "PredictionService host:port")
tf.app.flags.DEFINE_string("model", "", "The model name")
tf.app.flags.DEFINE_string("data", "", "The json file for inference")
tf.app.flags.DEFINE_float("timeout", 10.0, "The timeout of gRPC request")
FLAGS = tf.app.flags.FLAGS


def get_tensor_values(tensor):
  """Get TensorProto values
  Args:
    tensor: The TensorProto object.

  Returns:
    The list of values with specified type.
  """
  # The int of dtype refers to https://github.com/tensorflow/tensorflow/blob/master/tensorflow/core/framework/types.proto.
  if tensor.dtype == 1:
    return tensor.float_val
  elif tensor.dtype == 2:
    return tensor.double_val
  elif tensor.dtype == 3:
    return tensor.int_val
  elif tensor.dtype == 4:
    return tensor.int_val
  elif tensor.dtype == 5:
    return tensor.int_val
  elif tensor.dtype == 6:
    return tensor.int_val
  elif tensor.dtype == 7:
    return tensor.string_val
  elif tensor.dtype == 8:
    return tensor.scomplex_val
  elif tensor.dtype == 9:
    return tensor.int64_val
  elif tensor.dtype == 10:
    return tensor.bool_val
  elif tensor.dtype == 11:
    return tensor.int_val
  elif tensor.dtype == 12:
    return tensor.int_val
  elif tensor.dtype == 13:
    return tensor.int_val
  elif tensor.dtype == 14:
    return tensor.float_val
  elif tensor.dtype == 15:
    return tensor.int_val
  elif tensor.dtype == 16:
    return tensor.int_val
  elif tensor.dtype == 17:
    return tensor.int_val
  elif tensor.dtype == 18:
    return tensor.dcomplex_val
  elif tensor.dtype == 19:
    return tensor.half_val
  else:
    return None


def predict(server, model, data, timeout=10.0):
  """Request generic gRPC server with specified data.
 
  Args:
    server: The address of server. Example: "localhost:9000".
    model: The name of the model. Example: "mnist".
    data: The json data to request. Example: {"keys_dtype": "int32", "keys": [[1], [2]]}.

  Returns:
    The predict result in dictionary format. Example: {"keys": [1, 2]}.
  """
  host, port = server.split(":")
  channel = implementations.insecure_channel(host, int(port))
  stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

  request = predict_pb2.PredictRequest()
  request.model_spec.name = model
  for k, v in data.items():
    if k.endswith("_dtype") == False:
      numpy_data = np.array(v)
      dtype = data[k + "_dtype"]
      request.inputs[k].CopyFrom(tensor_util.make_tensor_proto(numpy_data,
                                                               dtype=dtype))

  result = stub.Predict(request, timeout)
  result_dict = {}
  for k, v in result.outputs.items():
    result_dict[k] = get_tensor_values(v)
  return result_dict


def main():
  server = FLAGS.server
  model = FLAGS.model
  timeout = FLAGS.timeout
  json_file = FLAGS.data
  if os.path.isfile(json_file):
    with open(json_file) as f:
      data = json.load(f)
  else:
    print("The data file doesn't exist, exit")
    exit(1)

  result = predict(server, model, data, timeout)
  print(result)


if __name__ == "__main__":
  main()
