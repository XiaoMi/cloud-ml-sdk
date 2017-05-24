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


class TensorboardService(object):
  """Class for tensorboard method.
  """

  def __init__(self,
               tensorboard_name,
               logdir,
               framework=None,
               framework_version=None,
               docker_image=None,
               docker_command=None,
               node_selector_key=None,
               node_selector_value=None):
    self.tensorboard_name = tensorboard_name
    self.logdir = logdir
    self.framework = framework
    self.framework_version = framework_version
    self.docker_image = docker_image
    self.docker_command = docker_command
    self.node_selector_key = node_selector_key
    self.node_selector_value = node_selector_value

  @property
  def tensorboard_name(self):
    return self._tensorboard_name

  @tensorboard_name.setter
  def tensorboard_name(self, value):
    if not isinstance(value, str):
      raise ValueError("tensorboard_name must be a string!")
    if value == "":
      raise ValueError("tensorboard_name cannot be None!")
    if not util.check_kube_resource_name_regex(value):
      raise StandardError("tensorboard_name must match {}.".format(
          util.kube_resource_name_regex))
    self._tensorboard_name = value

  @property
  def logdir(self):
    return self._logdir

  @logdir.setter
  def logdir(self, value):
    if not isinstance(value, str):
      raise ValueError("logdir must be a string!")
    if value == "":
      raise ValueError("logdir cannot be None!")
    self._logdir = value

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
        "tensorboard_name": self._tensorboard_name,
        "logdir": self._logdir,
    }
    if self._docker_image is not None:
      data["docker_image"] = self._docker_image
    if self._docker_command is not None:
      data["docker_command"] = self._docker_command
    if self._framework is not None:
      data["framework"] = self._framework
    if self._framework_version is not None:
      data["framework_version"] = self._framework_version
    if self._node_selector_key:
      data["node_selector_key"] = self._node_selector_key
    if self._node_selector_value:
      data["node_selector_value"] = self._node_selector_value

    return json.dumps(data)
