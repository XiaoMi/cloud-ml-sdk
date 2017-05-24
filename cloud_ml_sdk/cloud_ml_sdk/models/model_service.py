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

import json
from . import constant
from . import util


class ModelService(object):
  """The model of model service.
  """

  def __init__(self,
               model_name,
               model_version,
               model_uri,
               model_args=None,
               cpu_limit=None,
               gpu_limit=None,
               memory_limit=None,
               framework=None,
               framework_version=None,
               docker_image=None,
               docker_command=None,
               replicas=None,
               prepare_command=None,
               finish_command=None,
               node_selector_key=None,
               node_selector_value=None):
    self.model_name = model_name
    self.model_version = model_version
    self.model_uri = model_uri
    self.model_args = model_args
    self.cpu_limit = cpu_limit
    self.gpu_limit = gpu_limit
    self.memory_limit = memory_limit
    self.framework = framework
    self.framework_version = framework_version
    self.docker_image = docker_image
    self.docker_command = docker_command
    self.replicas = replicas
    self.prepare_command = prepare_command
    self.finish_command = finish_command
    self.node_selector_key = node_selector_key
    self.node_selector_value = node_selector_value

  @property
  def model_name(self):
    return self._model_name

  @model_name.setter
  def model_name(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    if not util.check_kube_resource_name_regex(value):
      raise StandardError("model_name must match {}.".format(
          util.kube_resource_name_regex))
    self._model_name = value

  @property
  def model_version(self):
    return self._model_version

  @model_version.setter
  def model_version(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    self._model_version = value

  @property
  def model_uri(self):
    return self._model_uri

  @model_uri.setter
  def model_uri(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    self._model_uri = value

  @property
  def model_args(self):
    return self._model_args

  @model_args.setter
  def model_args(self, value):
    """Function for setting model_args.

    Args:
      value: The model arguments.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("model_args must be a string!")
    self._model_args = value

  @property
  def cpu_limit(self):
    return self._cpu_limit

  @cpu_limit.setter
  def cpu_limit(self, value):
    if value != None:
      if not isinstance(value, str):
        raise ValueError("cpu_limit must be a string!")
      if not value.replace(".", "", 1).isdigit():
        raise ValueError("cpu_limit must be a number!")
      digits = value.split(".")
      if len(digits) == 2 and len(digits[1]) > constant.QUOTA_ACCURACY_PLACE:
        raise StandardError(
            "The value of cpu_limit accurate to two decimal places, for example: {}".format(
                round(
                    float(value), constant.QUOTA_ACCURACY_PLACE)))
    self._cpu_limit = value

  @property
  def gpu_limit(self):
    return self._gpu_limit

  @gpu_limit.setter
  def gpu_limit(self, value):
    if value != None:
      if not (isinstance(value, int) and value > 0):
        raise ValueError("gpu_limit must be a postive integer!")
    self._gpu_limit = value

  @property
  def memory_limit(self):
    return self._memory_limit

  @memory_limit.setter
  def memory_limit(self, value):
    if value != None:
      if not isinstance(value, str):
        raise ValueError("memory_limit must be a string")
      unit = value[-1:]
      float_value = value[:-1]
      if unit not in constant.CLOUDML_MEMORY_UNITS:
        raise ValueError("memory_limit unit must be one of %s!" %
                         constant.CLOUDML_MEMORY_UNITS)
      if not float_value.replace(".", "", 1).isdigit():
        raise ValueError("memory_limit must be a number!")
      digits = float_value.split(".")
      if len(digits) == 2 and len(digits[1]) > constant.QUOTA_ACCURACY_PLACE:
        raise StandardError(
            "The value of memory_limit accurate to two decimal places, for example: {}".format(
                round(
                    float(float_value), constant.QUOTA_ACCURACY_PLACE)))
    self._memory_limit = value

  @property
  def framework(self):
    return self._framework

  @framework.setter
  def framework(self, value):
    """Function for setting framework.

    Args:
      value: The framework.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Must be a string!")
    self._framework = value

  @property
  def framework_version(self):
    return self._framework_version

  @framework_version.setter
  def framework_version(self, value):
    """Function for setting version of framework.

    Args:
      value: The version of framework.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Must be a string!")
    self._framework_version = value

  @property
  def docker_image(self):
    return self._docker_image

  @docker_image.setter
  def docker_image(self, value):
    """Function for setting docker_image.

    Args:
      value: The docker_image.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Must be a string!")
    self._docker_image = value

  @property
  def docker_command(self):
    return self._docker_command

  @docker_command.setter
  def docker_command(self, value):
    """Function for setting docker_command.

    Args:
      value: The docker_command.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("Must be a string!")
    self._docker_command = value

  @property
  def replicas(self):
    return self._replicas

  @replicas.setter
  def replicas(self, value):
    """Function for setting replicas.

    Args:
      value: The replicas num.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not (isinstance(value, int) and value > 0):
        raise ValueError("replicas must be a postive integer!")
    self._replicas = value

  @property
  def prepare_command(self):
    return self._prepare_command

  @prepare_command.setter
  def prepare_command(self, value):
    """Function for set prepare_command.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not string instance or empty.
    """
    if value == "":
      raise ValueError("Prepare command can not be None!")
    self._prepare_command = value

  @property
  def finish_command(self):
    return self._finish_command

  @finish_command.setter
  def finish_command(self, value):
    """Function for set finish_command.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not string instance or empty.
    """
    if value == "":
      raise ValueError("Finish command can not be None!")
    self._finish_command = value

  @property
  def node_selector_key(self):
    return self._node_selector_key

  @node_selector_key.setter
  def node_selector_key(self, value):
    """Function for set node_selector_key.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not string instance or empty.
    """
    if value == "":
      raise ValueError("Node selector key can not be None!")
    self._node_selector_key = value

  @property
  def node_selector_value(self):
    return self._node_selector_value

  @node_selector_value.setter
  def node_selector_value(self, value):
    """Function for set node_selector_value.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not string instance or empty.
    """
    if value == "":
      raise ValueError("Node selector value can not be None!")
    self._node_selector_value = value

  def get_json_data(self):
    data = {
        "model_name": self._model_name,
        "model_version": self._model_version,
        "model_uri": self._model_uri
    }
    if self._model_args:
      data["model_args"] = self._model_args
    if self._cpu_limit:
      data["cpu_limit"] = self._cpu_limit
    if self._gpu_limit:
      data["gpu_limit"] = self._gpu_limit
    if self._memory_limit:
      data["memory_limit"] = self._memory_limit
    if self._framework:
      data["framework"] = self._framework
    if self._framework_version:
      data["framework_version"] = self._framework_version
    if self._docker_image:
      data["docker_image"] = self._docker_image
    if self._docker_command:
      data["docker_command"] = self._docker_command
    if self._replicas:
      data["replicas"] = self._replicas
    if self._prepare_command:
      data["prepare_command"] = self._prepare_command
    if self._finish_command:
      data["finish_command"] = self._finish_command
    if self._node_selector_key:
      data["node_selector_key"] = self._node_selector_key
    if self._node_selector_value:
      data["node_selector_value"] = self._node_selector_value

    return json.dumps(data)
