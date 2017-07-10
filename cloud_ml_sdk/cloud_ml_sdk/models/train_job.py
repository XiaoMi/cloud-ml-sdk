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


class TrainJob(object):
  """Class for train method.

  A TrainJob instance provides variables getter and setter apis. After
  specifying the necessary parameters, users can call start_run func to start
  the train job.
  """

  def __init__(self,
               job_name,
               module_name,
               trainer_uri,
               job_args=None,
               cpu_limit=None,
               gpu_limit=None,
               memory_limit=None,
               ps_count=None,
               worker_count=None,
               framework=None,
               framework_version=None,
               docker_image=None,
               docker_command=None,
               volume_type=None,
               volume_path=None,
               mount_path=None,
               mount_read_only=None,
               prepare_command=None,
               finish_command=None,
               node_selector_key=None,
               node_selector_value=None):
    """Creates a new TrainJob with given definition.

    The `job_name`, `module_name` and `trainer_uri` arguments must be provided
    when the object is creating.

    Args:
      job_name: The name of specific job.
      module_name: The name of module.
      trainer_uri: The uri that save the source code of job.
    """
    self.job_name = job_name
    self.module_name = module_name
    self.trainer_uri = trainer_uri

    self.job_args = job_args
    self.cpu_limit = cpu_limit
    self.memory_limit = memory_limit
    self.gpu_limit = gpu_limit
    self.ps_count = ps_count
    self.worker_count = worker_count
    self.framework = framework
    self.framework_version = framework_version
    self.docker_image = docker_image
    self.docker_command = docker_command
    self.volume_type = volume_type
    self.volume_path = volume_path
    self.mount_path = mount_path
    self.mount_read_only = mount_read_only
    self.prepare_command = prepare_command
    self.finish_command = finish_command
    self.node_selector_key = node_selector_key
    self.node_selector_value = node_selector_value

  @property
  def job_name(self):
    return self._job_name

  @job_name.setter
  def job_name(self, value):
    """Function for setting job_name.

    Args:
      value: String type value that is going to be set to job_name. Which
             cannot be empty.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if not isinstance(value, str):
      raise ValueError("job_name must be a string!")
    if value == "":
      raise ValueError("job_name cannot be None!")
    if not util.check_kube_resource_name_regex(value):
      raise StandardError("job_name must match {}.".format(
          util.kube_resource_name_regex))
    self._job_name = value

  @property
  def module_name(self):
    return self._module_name

  @module_name.setter
  def module_name(self, value):
    """Function for setting module_name.

    Args:
      value: String type value that is going to be set to module_name. Which
             cannot be empty.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if not isinstance(value, str):
      raise ValueError("module_name must be a string!")
    if value == "":
      raise ValueError("module_name cannot be None!")
    self._module_name = value

  @property
  def trainer_uri(self):
    return self._trainer_uri

  @trainer_uri.setter
  def trainer_uri(self, value):
    """Function for setting trainer_uri.

    Args:
      value: String type value that is going to be set to trainer_uri. Which
             cannot be empty.

    Raises:
      ValueError: If value is not str instance or does not start with `http://`
                   or `https://`.
    """
    if not isinstance(value, str):
      raise ValueError("trainer_uri must be a string!")
    self._trainer_uri = value

  @property
  def job_args(self):
    return self._job_args

  @job_args.setter
  def job_args(self, value):
    """Function for setting job_args.

    Args:
      value: The job arguments.

    Raises:
      ValueError: If value is not string instance.
    """
    if value != None:
      if not isinstance(value, str):
        raise ValueError("job_args must be a string!")
    self._job_args = value

  @property
  def cpu_limit(self):
    return self._cpu_limit

  @cpu_limit.setter
  def cpu_limit(self, value):
    """Function for setting cpu_limit.

    Args:
      value: Cpu limit.

    Raises:
      ValueError: If value is not a positive number.
    """
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
  def memory_limit(self):
    return self._memory_limit

  @memory_limit.setter
  def memory_limit(self, value):
    """Function for setting memory_limit.

    Args:
      value: Memory limit.

    Raises:
      ValueError: Doesn't end with K, M or G.
    """
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
  def gpu_limit(self):
    return self._gpu_limit

  @gpu_limit.setter
  def gpu_limit(self, value):
    """Function for setting gpu_limit.

    Args:
      value: GPU limit.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value >= 0):
        raise ValueError("gpu_limit must be a nonnegative integer!")
    self._gpu_limit = value

  @property
  def ps_count(self):
    return self._ps_count

  @ps_count.setter
  def ps_count(self, value):
    """Function for setting ps_count.

    Args:
      value: TensorFlow PS count.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value > 0):
        raise ValueError("ps_count must be a positive integer!")
    self._ps_count = value

  @property
  def worker_count(self):
    return self._worker_count

  @worker_count.setter
  def worker_count(self, value):
    """Function for setting worker_count.

    Args:
      value: TensorFlow worker count.

    Raises:
      ValueError: If value is not a positive number.
    """
    if value != None:
      if not (isinstance(value, int) and value > 0):
        raise ValueError("worker_count must be a positive integer!")
    self._worker_count = value

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
  def volume_type(self):
    return self._volume_type

  @volume_type.setter
  def volume_type(self, value):
    """Function for set.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if value == "":
      raise ValueError("Volume type can not be None!")
    self._volume_type = value

  @property
  def volume_path(self):
    return self._volume_path

  @volume_path.setter
  def volume_path(self, value):
    """Function for set.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if value == "":
      raise ValueError("Volume path can not be None!")
    self._volume_path = value

  @property
  def mount_path(self):
    return self._mount_path

  @mount_path.setter
  def mount_path(self, value):
    """Function for set.

    Args:
      value: String value.

    Raises:
      ValueError: If value is not str instance or empty.
    """
    if value == "":
      raise ValueError("Mount path can not be None!")
    self._mount_path = value

  @property
  def mount_read_only(self):
    return self._mount_read_only

  @mount_read_only.setter
  def mount_read_only(self, value):
    """Function for set.

    Args:
      value: Boolean value.

    Raises:
      ValueError: If value is not boolean instance or empty.
    """
    if value != None and type(value) != bool:
      raise ValueError("Mount read only should be boolean!")
    self._mount_read_only = value

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
    """Get the needed train job data after setting necessary varibles.

    Returns:
      data: The json data which is necessary for the train job.

    Raises:
      ValueError: If endpoint is not a string starting with `http://`.
                  If _job_name, _module_name or _trainer_uri is empty.
    """
    data = {
        "job_name": self._job_name,
        "module_name": self._module_name,
        "trainer_uri": self._trainer_uri,
    }
    if self._job_args is not None:
      data["job_args"] = self._job_args
    if self._cpu_limit is not None:
      data["cpu_limit"] = self._cpu_limit
    if self._memory_limit is not None:
      data["memory_limit"] = self._memory_limit
    if self._gpu_limit is not None:
      data["gpu_limit"] = self._gpu_limit
    if self._ps_count is not None:
      data["ps_count"] = self._ps_count
    if self._worker_count is not None:
      data["worker_count"] = self._worker_count
    if self._docker_image is not None:
      data["docker_image"] = self._docker_image
    if self._docker_command is not None:
      data["docker_command"] = self._docker_command
    if self._framework is not None:
      data["framework"] = self._framework
    if self._framework_version is not None:
      data["framework_version"] = self._framework_version
    if self._volume_type is not None:
      data["volume_type"] = self._volume_type
    if self._volume_path is not None:
      data["volume_path"] = self._volume_path
    if self._mount_path is not None:
      data["mount_path"] = self._mount_path
    if self._mount_read_only is not None:
      data["mount_read_only"] = self._mount_read_only
    if self._prepare_command:
      data["prepare_command"] = self._prepare_command
    if self._finish_command:
      data["finish_command"] = self._finish_command
    if self._node_selector_key:
      data["node_selector_key"] = self._node_selector_key
    if self._node_selector_value:
      data["node_selector_value"] = self._node_selector_value

    return json.dumps(data)
