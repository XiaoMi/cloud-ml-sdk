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


class DevServer(object):
  """The model of dev server.
  """

  def __init__(self,
               dev_name,
               password,
               cpu_limit=None,
               gpu_limit=None,
               memory_limit=None,
               framework=None,
               framework_version=None,
               docker_image=None,
               docker_command=None):
    self.dev_name = dev_name
    self.password = password
    self.cpu_limit = cpu_limit
    self.gpu_limit = gpu_limit
    self.memory_limit = memory_limit
    self.framework = framework
    self.framework_version = framework_version
    self.docker_image = docker_image
    self.docker_command = docker_command

  @property
  def dev_name(self):
    return self._dev_name

  @dev_name.setter
  def dev_name(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    if not util.check_kube_resource_name_regex(value):
      raise StandardError("dev_name must match {}.".format(
          util.kube_resource_name_regex))
    self._dev_name = value

  @property
  def password(self):
    return self._password

  @password.setter
  def password(self, value):
    if not isinstance(value, str):
      raise ValueError("The type should be string")
    self._password = value

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

  def get_json_data(self):
    data = {"dev_name": self._dev_name, "password": self.password}
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

    return json.dumps(data)
