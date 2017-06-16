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
import logging
import os
import getpass
import sys
import time
sys.path.append("../../")

from . import color_util
from . import constant
from cloud_ml_sdk.client import CloudMlClient
from cloud_ml_sdk.models.train_job import TrainJob
from cloud_ml_sdk.models.model_service import ModelService
from cloud_ml_sdk.models.dev_env import DevEnv
from cloud_ml_sdk.models.tensorboard_service import TensorboardService
from cloud_ml_sdk.models.quota import Quota
from cloud_ml_sdk.models.dev_server import DevServer

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("requests").setLevel(logging.WARNING)


def compatibility_input(obj):
  if sys.version_info > (3, 0):
    res = input(obj)
  else:
    res = raw_input(obj)
  return res


def authentication(access_key, secret_key, endpoint):
  client = CloudMlClient(access_key, secret_key, endpoint)
  response = client.authentication()
  if isinstance(response, str):
    return False
  else:
    return True


def init_config(args):
  """Set the initial config."""

  config_dir = os.path.join(os.path.expanduser("~"), ".config/xiaomi/")
  config_path = os.path.join(config_dir, "config")

  flag = "y"
  config_data = {}
  if os.path.exists(config_path):
    try:
      with open(config_path) as data_file:
        config_data = json.load(data_file)
    except Exception as e:
      print(
          "~/.config/xiaomi/config already exists. But failed to load config file, exception: {}".format(
              e))
      print("You need to fix the config file by hand.")
      return
    flag = compatibility_input(
        "~/.config/xiaomi/config already exists. Reset? (y/N): ")

  if flag == "y" or flag == "Y":
    while True:
      access_key = compatibility_input("Please input access key: ")
      secret_key = getpass.getpass(
          "Please input secret key (will not be echoed): ")
      if access_key.find("/") >= 0 or secret_key.find("/") >= 0:
        print(color_util.colorize_warning("\nATTENSION:"))
        print(color_util.colorize_warning(
            "The access key and secret key with slashes may cause fault in getting data from fds when use tensorflow framework!\n"))

      ## commented out for eco-cloud sdk, do not want to leak the internal endpoint
      # cloudml_endpoint = compatibility_input(
      #       "Please input cloudml endpoint[default: {}]: ".format(
      #       constant.DEFAULT_CLOUDML_API_ENDPOINT)) or constant.DEFAULT_CLOUDML_API_ENDPOINT

      cloudml_endpoint = compatibility_input(
          "Please input cloudml endpoint: ")

      if compatibility_input(
          "\nTest access with supplied credentials? [y/N]: ") in [
              "y", "Y"
          ] and not authentication(access_key, secret_key, cloudml_endpoint):
        print("ERROR: Test failed, invalid config message.")
        if not compatibility_input("\nRetry configuration? [y/N]: ") in ["y",
                                                                         "Y"]:
          break
      else:
        print("Test successfully!")
        break

    if compatibility_input("\nSave settings? [y/N]: ") in ["y", "Y"]:
      config_data["xiaomi_access_key_id"] = access_key
      config_data["xiaomi_secret_access_key"] = secret_key
      config_data["xiaomi_cloudml_endpoint"] = cloudml_endpoint
      if not os.path.exists(config_dir):
        os.makedirs(config_dir)
      with open(config_path, "w") as outfile:
        json.dump(config_data, outfile, indent=4)
      print("Successfully initialize config file in path: {}".format(
          config_path))
    else:
      print("Configuration aborted. Changes were NOT saved.")
      return
  else:
    print("cloudml init operation exit without any modification.")


def get_org_id(args):
  """Get org_id by access_key and secret_key in config file."""

  client = CloudMlClient()
  response = client.get_org_id()
  if isinstance(response, str):
    print("response: {}".format(response))
  else:
    print("Your org_id is: {}".format(response.get("org_id")))


def print_train_job_info(train_job):
  """Print train job in customed format.

  Args:
    train_job: The dictionary of response train job data.
  """
  print("{:16} {}".format("Org id:", train_job["org_id"]))
  print("{:16} {}".format("Org name:", train_job["org_name"]))
  print("{:16} {}".format("Job name:", train_job["job_name"]))
  print("{:16} {}".format("Module name:", train_job["module_name"]))
  print("{:16} {}".format("Trainer uri:", train_job["trainer_uri"]))
  print("{:16} {}".format("Job args:", train_job["job_args"]))
  print("{:16} {}".format("CPU limit:", train_job["cpu_limit"]))
  print("{:16} {}".format("Memory limit:", train_job["memory_limit"]))
  print("{:16} {}".format("GPU limit:", train_job["gpu_limit"]))
  print("{:16} {}".format("Docker image:", train_job["docker_image"]))
  print("{:16} {}".format("Docker command:", train_job["docker_command"]))
  print("{:16} {}".format("Framework:", train_job["framework"]))
  print("{:16} {}".format("Framework version:", train_job[
      "framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(train_job["state"])))
  print("{:16} {}".format("Create time:", train_job["create_time"]))
  print("{:16} {}".format("Update time:", train_job["update_time"]))
  if train_job["cluster_name"]:
    print("{:16} {}".format("Cluster name:", train_job["cluster_name"]))
  if train_job["service_port"]:
    print("{:16} {}".format("Service port:", train_job["service_port"]))
  if train_job["cluster_env_var"]:
    print("{:16} {}".format("Cluter environment variables:", train_job[
        "cluster_env_var"]))
  if train_job["hyperparameters_name"]:
    print("{:16} {}".format("Hyperparameters name:", train_job[
        "hyperparameters_name"]))
  if train_job["hyperparameters_goal"]:
    print("{:16} {}".format("Hyperparameters goal:", train_job[
        "hyperparameters_goal"]))
  if train_job["hyperparameters_params"]:
    print("{:16} {}".format("Hyperparameters params:", train_job[
        "hyperparameters_params"]))
  print("{:16} {}".format("Volume type:", train_job["volume_type"]))
  print("{:16} {}".format("Volume path:", train_job["volume_path"]))
  print("{:16} {}".format("Mount path:", train_job["mount_path"]))
  print("{:16} {}".format("Mount read only:", train_job["mount_read_only"]))
  print("{:16} {}".format("Prepare command:", train_job["prepare_command"]))
  print("{:16} {}".format("Finish command:", train_job["finish_command"]))
  print("{:16} {}".format("Node selector key:", train_job["node_selector_key"]))
  print("{:16} {}".format("Node selector value:", train_job["node_selector_value"]))


def print_model_service_info(model):
  """Print model service in customed format.

  Args:
    model: The dictionary of response model service data.
  """
  print("{:16} {}".format("Org id:", model["org_id"]))
  print("{:16} {}".format("Org name:", model["org_name"]))
  print("{:16} {}".format("Model name:", model["model_name"]))
  print("{:16} {}".format("Model version:", model["model_version"]))
  print("{:16} {}".format("Model uri:", model["model_uri"]))
  print("{:16} {}".format("Model args:", model["model_args"]))
  print("{:16} {}".format("Service port:", model["service_port"]))
  print("{:16} {}".format("Replicas:", model["replicas"]))
  print("{:16} {}( x {})".format("CPU limit:", model["cpu_limit"], model[
      "replicas"]))
  print("{:16} {}( x {})".format("Memory limit:", model["memory_limit"], model[
      "replicas"]))
  print("{:16} {}( x {})".format("GPU limit:", model["gpu_limit"], model[
      "replicas"]))
  print("{:16} {}".format("Docker image:", model["docker_image"]))
  print("{:16} {}".format("Docker command:", model["docker_command"]))
  print("{:16} {}".format("Framework:", model["framework"]))
  print("{:16} {}".format("Framework version:", model["framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(model["state"])))
  print("{:16} {}".format("Create time:", model["create_time"]))
  print("{:16} {}".format("Update time:", model["update_time"]))
  print("{:16} {}".format("Address:", model["address"]))
  print("{:16} {}".format("Prepare command:", model["prepare_command"]))
  print("{:16} {}".format("Finish command:", model["finish_command"]))
  print("{:16} {}".format("Node selector key:", model["node_selector_key"]))
  print("{:16} {}".format("Node selector value:", model["node_selector_value"]))


def print_dev_env_info(dev_env):
  """Print dev_env in customed format.

  Args:
    dev_env: The dictionary of response dev env data.
  """
  print("{:16} {}".format("Org id:", dev_env["org_id"]))
  print("{:16} {}".format("Org name:", dev_env["org_name"]))
  print("{:16} {}".format("Dev name:", dev_env["dev_name"]))
  print("{:16} {}".format("Password:", dev_env["password"]))
  print("{:16} {}".format("Notebook port:", dev_env["notebook_port"]))
  print("{:16} {}".format("Ssh port:", dev_env["ssh_port"]))
  print("{:16} {}".format("CPU limit:", dev_env["cpu_limit"]))
  print("{:16} {}".format("Memory limit:", dev_env["memory_limit"]))
  print("{:16} {}".format("GPU limit:", dev_env["gpu_limit"]))
  print("{:16} {}".format("Docker image:", dev_env["docker_image"]))
  print("{:16} {}".format("Docker command:", dev_env["docker_command"]))
  print("{:16} {}".format("Framework:", dev_env["framework"]))
  print("{:16} {}".format("Framework version:", dev_env["framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(dev_env["state"])))
  print("{:16} {}".format("Create time:", dev_env["create_time"]))
  print("{:16} {}".format("Update time:", dev_env["update_time"]))
  print("{:16} {}".format("Address:", dev_env["address"]))
  print("{:16} {}".format("Ssh address:", dev_env["ssh_address"]))
  print("{:16} {}".format("Node selector key:", dev_env["node_selector_key"]))
  print("{:16} {}".format("Node selector value:", dev_env["node_selector_value"]))


def print_dev_server_info(dev_server):
  """Print dev_server in customed format.

  Args:
    dev_server: The dictionary of response dev server data.
  """
  print("{:16} {}".format("Org id:", dev_server["org_id"]))
  print("{:16} {}".format("Org name:", dev_server["org_name"]))
  print("{:16} {}".format("Dev name:", dev_server["dev_name"]))
  print("{:16} {}".format("Password:", dev_server["password"]))
  print("{:16} {}".format("Notebook port:", dev_server["notebook_port"]))
  print("{:16} {}".format("Ssh port:", dev_server["ssh_port"]))
  print("{:16} {}".format("CPU limit:", dev_server["cpu_limit"]))
  print("{:16} {}".format("Memory limit:", dev_server["memory_limit"]))
  print("{:16} {}".format("GPU limit:", dev_server["gpu_limit"]))
  print("{:16} {}".format("Docker image:", dev_server["docker_image"]))
  print("{:16} {}".format("Docker command:", dev_server["docker_command"]))
  print("{:16} {}".format("Framework:", dev_server["framework"]))
  print("{:16} {}".format("Framework version:", dev_server[
      "framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(dev_server["state"])))
  print("{:16} {}".format("Create time:", dev_server["create_time"]))
  print("{:16} {}".format("Update time:", dev_server["update_time"]))
  print("{:16} {}".format("Address:", dev_server["address"]))
  print("{:16} {}".format("Ssh address:", dev_server["ssh_address"]))


def print_tensorboard_info(tensorboard):
  """Print tensorboard in customed format.

  Args:
    tensorboard: The dictionary of response tensorboard data.
  """
  print("{:16} {}".format("Org id:", tensorboard["org_id"]))
  print("{:16} {}".format("Org name:", tensorboard["org_name"]))
  print("{:16} {}".format("Tensorboard name:", tensorboard[
      "tensorboard_name"]))
  print("{:16} {}".format("Logdir:", tensorboard["logdir"]))
  print("{:16} {}".format("Service port:", tensorboard["service_port"]))
  print("{:16} {}".format("Docker image:", tensorboard["docker_image"]))
  print("{:16} {}".format("Docker command:", tensorboard["docker_command"]))
  print("{:16} {}".format("Framework:", tensorboard["framework"]))
  print("{:16} {}".format("Framework version:", tensorboard[
      "framework_version"]))
  print("{:16} {}".format("State:", color_util.colorize_state(tensorboard["state"])))
  print("{:16} {}".format("Create time:", tensorboard["create_time"]))
  print("{:16} {}".format("Update time:", tensorboard["update_time"]))
  print("{:16} {}".format("Address:", tensorboard["address"]))
  print("{:16} {}".format("Node selector key:", tensorboard["node_selector_key"]))
  print("{:16} {}".format("Node selector value:", tensorboard["node_selector_value"]))


def print_quota_info(quota):
  """Print quota in customed format.

  Args:
    quota: The dictionary of response quota data.
  """
  total_memory_quota = "INF" if quota[
      "total_memory_quota"] == constant.INF_TOTAL_MEMORY_QUOTA else quota[
          "total_memory_quota"]
  total_cpu_quota = "INF" if quota[
      "total_cpu_quota"] == constant.INF_TOTAL_CPU_QUOTA else quota[
          "total_cpu_quota"]
  total_gpu_quota = "INF" if quota[
      "total_gpu_quota"] == constant.INF_TOTAL_GPU_QUOTA else quota[
          "total_gpu_quota"]
  train_count_quota = "INF" if quota[
      "train_count_quota"] == constant.INF_JOB_COUNT else quota[
          "train_count_quota"]
  model_count_quota = "INF" if quota[
      "model_count_quota"] == constant.INF_JOB_COUNT else quota[
          "model_count_quota"]
  dev_count_quota = "INF" if quota[
      "dev_count_quota"] == constant.INF_JOB_COUNT else quota[
          "dev_count_quota"]

  print("{:16} {}".format("Org id:", quota["org_id"]))
  print("{:16} {:32} {:32} {:32} {:32} {:32}".format(
      "", "Memory / Used", "CPU / Used", "GPU / Used", "Tensorboard / Used",
      "Count / Used"))
  print("{:16} {:32} {:32} {:32} {:32} {:32}".format(
      "Train job", quota["train_memory_quota"] + " / " +
      quota["train_memory_used"], quota["train_cpu_quota"] + " / " + quota[
          "train_cpu_used"], quota["train_gpu_quota"] + " / " + quota[
              "train_gpu_used"], "- / -", train_count_quota + " / " + quota[
                  "train_count_used"]))
  print("{:16} {:32} {:32} {:32} {:32} {:32}".format(
      "Model service", quota["model_memory_quota"] + " / " +
      quota["model_memory_used"], quota["model_cpu_quota"] + " / " + quota[
          "model_cpu_used"], quota["model_gpu_quota"] + " / " + quota[
              "model_gpu_used"], "- / -", model_count_quota + " / " + quota[
                  "model_count_used"]))
  print("{:16} {:32} {:32} {:32} {:32} {:32}".format("Dev environment", quota[
      "dev_memory_quota"] + " / " + quota["dev_memory_used"], quota[
          "dev_cpu_quota"] + " / " + quota["dev_cpu_used"], quota[
              "dev_gpu_quota"] + " / " + quota[
                  "dev_gpu_used"], "- / -", dev_count_quota + " / " + quota[
                      "dev_count_used"]))
  print("{:16} {:32} {:32} {:32} {:32} {:32}".format(
      "Tensorboard", "- / -", "- / -", "- / -", quota["tensorboard_quota"] +
      " / " + quota["tensorboard_used"], "- / -"))

  print("{:16} {:32} {:32} {:32} {:32} {:32}".format(
      "Total quota", total_memory_quota + " / " + quota["total_memory_used"],
      total_cpu_quota + " / " + quota["total_cpu_used"], total_gpu_quota +
      " / " + quota["total_gpu_used"], "- / -", "- / -"))


def print_frameworks_info(framework):
  print("{:16} {}".format("FRAMEWORK", "FRAMEWORK"))
  for framework_name in framework:
    for index in range(len(framework[framework_name])):
      if index == 0:
        print("{:16} {}".format(framework_name, framework[framework_name][
            index]))
      else:
        print("{:16} {}".format("", framework[framework_name][index]))


def print_predict_result(result):
  """Print the predict result in customed format.

  Args:
    result: The predict result. Example: {u"predict": [30.00011444091797, 70.00050354003906], u"keys": [10, 20]}
  """
  print("Predictions:")
  for i in range(len(result.values()[0])):
    print_divider = True
    for k, v in result.items():
      if print_divider:
        print("{} {}: {}".format("-", k, v[i]))
        print_divider = False
      else:
        print("{} {}: {}".format(" ", k, v[i]))


def print_hyperparameter_data_result(result):
  """Print the hyperparameter result in customed format.

  Args:
    result: The result. Example: {"best_trials": {}, "goal": "MINIMIZE", "trialCount": 4, "trial": [{}]}
                                 Each trial contains {"metric": 0.08, "params": "--foo=bar", "step": 100}
  """
  print("Goal: {}".format(result["goal"]))
  print("Trial count: {}".format(result["trialCount"]))
  print("Best trial:")
  print("{:8} Metrics: {}".format("", result["best_trials"]["metric"]))
  print("{:8} Params: {}".format("", result["best_trials"]["params"]))
  print("{:8} Step: {}".format("", result["best_trials"]["step"]))
  print("{:8} State: {}".format("", result["best_trials"]["state"]))

  trials = result["trials"]
  for i in range(len(trials)):
    print("Trial {}:".format(i))
    print("{:8} Metrics: {}".format("", trials[i]["metric"]))
    print("{:8} Params: {}".format("", trials[i]["params"]))
    print("{:8} Step: {}".format("", trials[i]["step"]))
    print("{:8} State: {}".format("", trials[i]["state"]))


def print_kubernetes_events(events):
  """Print the events logs from Kubernetes API.

  Args:
    events: The list of event. Example: {"count": 1, "firstTimestamp": "2017-02-20T06:16:39Z"}
  """
  print("{:20} {:20} {:8} {:32} {:8} {:8} {}".format(
      "FirstTimestamp", "LastTimestamp", "Count", "Name", "Type", "Reason",
      "Message"))
  for event in events:
    print("{:20} {:20} {:8} {:32} {:8} {:8} {}".format(event[
        "firstTimestamp"], event["lastTimestamp"], event["count"], event[
            "involvedObject"]["name"], event["type"], event["reason"], event[
                "message"]))


def print_metrics_result(metrics):
  """Print the metrics result.

  Args:
    metrics: The metrics.
  """
  print("{:20} {} %".format("CPU:", metrics["cpu"]))
  print("{:20} {} Bytes".format("Memory:", metrics["memory"]))
  print("{:20} {} Bytes".format("Network receive:", metrics["network_receive"]))
  print("{:20} {} Bytes".format("Network transmit:", metrics["network_transmit"]))


def list_jobs(args):
  """List train jobs."""

  client = CloudMlClient()
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_train_jobs = client.list_train_jobs(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_train_jobs = client.list_train_jobs(args.org_id)
  else:
    response_train_jobs = client.list_train_jobs()
  if not isinstance(response_train_jobs, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      print("{:16} {:16} {:32} {:16} {:32} {:32}".format(
          "ORG ID", "ORG NAME", "JOB_NAME", "STATE", "CREATED", "UPDATED"))
      for train_job in response_train_jobs:
        print("{:<16} {:16} {:32} {:16} {:32} {:32}".format(train_job[
            "org_id"], train_job["org_name"], train_job["job_name"],
            color_util.colorize_state(train_job["state"]),
            train_job["create_time"], train_job["update_time"]))
    else:
      print("{:32} {:16} {:32} {:32}".format("JOB_NAME", "STATE", "CREATED",
                                             "UPDATED"))
      for train_job in response_train_jobs:
        print("{:32} {:16} {:32} {:32}".format(train_job[
            "job_name"], color_util.colorize_state(train_job["state"]),
            train_job["create_time"], train_job["update_time"]))
  else:
    print("response: {}".format(response_train_jobs))


def submit_job(args):
  """Submit the job."""

  client = CloudMlClient()
  if args.filename:
    with open(args.filename) as f:
      # TODO: Check file format and verify the items
      json_data = json.dumps(json.load(f))
      if not (("job_name" in json_data) and ("module_name" in json_data) and
              ("trainer_uri" in json_data)):
        print(
            "ERROR: parameters job_name, module_name and trainer_uri are necessary.")
        return
      if args.watch:
        job_name = json.loads(json_data).get("job_name")
  else:
    if not (args.job_name and args.module_name and args.trainer_uri):
      print(
          "ERROR: parameters job_name, module_name and trainer_uri cannot be None.")
      return
    train_job = TrainJob(args.job_name, args.module_name, args.trainer_uri)

    if args.job_args:
      train_job.job_args = args.job_args
    if args.cpu_limit:
      train_job.cpu_limit = args.cpu_limit
    if args.memory_limit:
      train_job.memory_limit = args.memory_limit
    if args.gpu_limit:
      train_job.gpu_limit = int(args.gpu_limit)
    if args.ps_count:
      train_job.ps_count = int(args.ps_count)
    if args.worker_count:
      train_job.worker_count = int(args.worker_count)
    if args.framework:
      train_job.framework = args.framework
    if args.framework_version:
      train_job.framework_version = args.framework_version
    if args.docker_image:
      train_job.docker_image = args.docker_image
    if args.docker_command:
      train_job.docker_command = args.docker_command
    if args.volume_type:
      train_job.volume_type = args.volume_type
    if args.volume_path:
      train_job.volume_path = args.volume_path
    if args.mount_path:
      train_job.mount_path = args.mount_path
    if args.mount_read_only:
      if args.mount_read_only == "true" or args.mount_read_only == "True":
        train_job.mount_read_only = True
      else:
        train_job.mount_read_only = False
    if args.prepare_command:
      train_job.prepare_command = args.prepare_command
    if args.finish_command:
      train_job.finish_command = args.finish_command
    if args.node_selector_key:
      train_job.node_selector_key = args.node_selector_key
    if args.node_selector_value:
      train_job.node_selector_value = args.node_selector_value

    json_data = train_job.get_json_data()

    if args.watch:
      job_name = args.job_name

  response = client.submit_train_job(json_data)
  if not isinstance(response, str):
    print_train_job_info(response)
    if args.watch:
      print("\nThe job has submitted, feel free to Ctrl+C to stop watching\n")
      print("{:32} {:16} {:32} {:32}".format("JOB_NAME", "STATE", "CREATED",
                                             "UPDATED"))
      while True:
        watch_response = client.describe_train_job(job_name)
        if not isinstance(watch_response, str):
          print("{:32} {:16} {:32} {:32}".format(watch_response[
                "job_name"], color_util.colorize_state(watch_response["state"]),
                watch_response["create_time"], watch_response["update_time"]))
          if watch_response["state"] == constant.JOB_STATE_COMPLETED:
            return
          try:
            time.sleep(constant.JOB_WATCH_INTERVAL)
          except KeyboardInterrupt:
            return
        else:
          return
  else:
    print("response: {}".format(response))


def describe_job(args):
  """Describe the job."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.describe_train_job(args.job_name, args.org_id)
  else:
    response = client.describe_train_job(args.job_name)
  if not isinstance(response, str):
    print_train_job_info(response)
  else:
    print("response: {}".format(response))


def get_job_logs(args):
  """Get the logs of the job."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.get_train_job_logs(args.job_name, args.org_id)
  else:
    response = client.get_train_job_logs(args.job_name)
  if not isinstance(response, str):
    print(response["logs"])
  else:
    print("response: {}".format(response))


def get_job_metrics(args):
  """Get the metrics of the job."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.get_train_job_metrics(args.job_name, args.org_id)
  else:
    response = client.get_train_job_metrics(args.job_name)
  if not isinstance(response, str):
    print_metrics_result(response)
  else:
    print("response: {}".format(response))


def get_job_hyperparameters_data(args):
  """Get hyperparameters data of the job."""

  client = CloudMlClient()
  response = client.get_train_job_hyperparameters_data(args.job_name)
  if not isinstance(response, str):
    print_hyperparameter_data_result(response)
  else:
    print("response: {}".format(response))


def delete_job(args):
  """Delete the job."""

  client = CloudMlClient()
  response = client.delete_train_job(args.job_name)
  print(response)


def get_train_job_events(args):
  """Get events of the train job."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.get_train_job_events(args.job_name, args.org_id)
  else:
    response = client.get_train_job_events(args.job_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
  else:
    print("response: {}".format(response))


def list_models(args):
  """List model services."""

  client = CloudMlClient()
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_models = client.list_model_services(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_models = client.list_model_services(args.org_id)
  else:
    response_models = client.list_model_services()
  if not isinstance(response_models, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      print("{:16} {:16} {:32} {:16} {:32} {:16} {:32} {:32}".format(
          "ORG ID", "ORG NAME", "MODEL_NAME", "MODEL_VERSION", "ADDRESS",
          "STATE", "CREATED", "UPDATED"))
      for model in response_models:
        print("{:16} {:16} {:32} {:16} {:32} {:16} {:32} {:32}".format(model[
            "org_id"], model["org_name"], model["model_name"], model[
            "model_version"], model["address"],
            color_util.colorize_state(model["state"]), model[
            "create_time"], model["update_time"]))
    else:
      print("{:32} {:16} {:32} {:16} {:32} {:32}".format(
          "MODEL_NAME", "MODEL_VERSION", "ADDRESS", "STATE", "CREATED",
          "UPDATED"))
      for model in response_models:
        print("{:32} {:16} {:32} {:16} {:32} {:32}".format(model[
            "model_name"], model["model_version"], model["address"],
            color_util.colorize_state(model["state"]),
            model["create_time"], model["update_time"]))
  else:
    print("response: {}".format(response_models))


def create_model(args):
  """Create the model service."""

  client = CloudMlClient()
  model = ModelService(args.model_name, args.model_version, args.model_uri)

  if args.model_args:
    model.model_args = args.model_args
  if args.cpu_limit:
    model.cpu_limit = args.cpu_limit
  if args.memory_limit:
    model.memory_limit = args.memory_limit
  if args.gpu_limit:
    model.gpu_limit = int(args.gpu_limit)
  if args.framework:
    model.framework = args.framework
  if args.framework_version:
    model.framework_version = args.framework_version
  if args.docker_image:
    model.docker_image = args.docker_image
  if args.docker_command:
    model.docker_command = args.docker_command
  if args.replicas:
    model.replicas = int(args.replicas)
  if args.prepare_command:
    model.prepare_command = args.prepare_command
  if args.finish_command:
    model.finish_command = args.finish_command
  if args.node_selector_key:
    model.node_selector_key = args.node_selector_key
  if args.node_selector_value:
    model.node_selector_value = args.node_selector_value
  if args.watch:
    model_name = args.model_name
    model_version = args.model_version

  response = client.create_model_service(model)
  if not isinstance(response, str):
    print_model_service_info(response)
    if args.watch:
      print("\nThe model is creating, feel free to Ctrl+C to stop watching\n")
      print("{:32} {:4} {:16} {:32} {:32}".format(
              "Model_NAME",
              "VERSION",
              "STATE",
              "CREATED",
              "UPDATED"))
      while True:
        watch_response = client.describe_model_service(model_name, model_version)
        if not isinstance(watch_response, str):
          print("{:32} {:4} {:16} {:32} {:32}".format(
                watch_response["model_name"],
                watch_response["model_version"],
                color_util.colorize_state(watch_response["state"]),
                watch_response["create_time"],
                watch_response["update_time"]))
          if watch_response["state"] == constant.MODEL_STATE_RUNNING:
            return
          try:
            time.sleep(constant.JOB_WATCH_INTERVAL)
          except KeyboardInterrupt:
            return
        else:
          return
  else:
    print("response: {}".format(response))


def describe_model(args):
  """Describe the model service."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.describe_model_service(args.model_name,
                                             args.model_version, args.org_id)
  else:
    response = client.describe_model_service(args.model_name,
                                             args.model_version)
  if not isinstance(response, str):
    print_model_service_info(response)
  else:
    print("response: {}".format(response))

def update_model(args):
  """Update the model service."""

  client = CloudMlClient()
  update_json = {}

  if args.replicas:
    update_json["replicas"] = int(args.replicas)

  if "org_id" in args:
    response = client.update_model_service(args.model_name,
                                           args.model_version,
                                           update_json,
                                           args.org_id)
  else:
    response = client.update_model_service(args.model_name,
                                           args.model_version,
                                           update_json)
  if not isinstance(response, str):
    print_model_service_info(response)
  else:
    print("response: {}".format(response))

def get_model_logs(args):
  """Get logs of the model service."""

  client = CloudMlClient()
  if "org_id" in args:
    if args.replica_index:
      response = client.get_model_service_logs(args.model_name, args.model_version, args.org_id, args.replica_index)
    else:
      response = client.get_model_service_logs(args.model_name, args.model_version, args.org_id)
  else:
    if args.replica_index:
      response = client.get_model_service_logs(args.model_name, args.model_version, replica_index=args.replica_index)
    else:
      response = client.get_model_service_logs(args.model_name, args.model_version)
  if not isinstance(response, str):
    if "error" in response:
      print(response['message'])
    else:
      print(response["logs"])


def get_model_metrics(args):
  """Get the metrics of the model service."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.get_model_service_metrics(args.model_name, args.model_version, args.org_id)
  else:
    response = client.get_model_service_metrics(args.model_name, args.model_version)
  if not isinstance(response, str):
    print_metrics_result(response)
  else:
    print("response: {}".format(response))


def delete_model(args):
  """Delete the model service."""

  client = CloudMlClient()
  response = client.delete_model_service(args.model_name, args.model_version)
  print(response)


def get_model_service_events(args):
  """Get events of the model service."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.get_model_service_events(args.model_name,
                                               args.model_version, args.org_id)
  else:
    response = client.get_model_service_events(args.model_name,
                                               args.model_version)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
  else:
    print("response: {}".format(response))


def list_tensorboard_services(args):
  """List tensorboard_services."""

  client = CloudMlClient()
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_tensorboard = client.list_tensorboard_services(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_tensorboard = client.list_tensorboard_services(args.org_id)
  else:
    response_tensorboard = client.list_tensorboard_services()

  if not isinstance(response_tensorboard, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      print("{:16} {:16} {:32} {:32} {:16} {:32} {:32}".format(
          "ORG ID", "ORG NAME", "TENSORBOARD_NAME", "ADDRESS", "STATE",
          "CREATED", "UPDATED"))
      for tensorboard in response_tensorboard:
        print("{:16} {:16} {:32} {:32} {:16} {:32} {:32}".format(tensorboard[
            "org_id"], tensorboard["org_name"], tensorboard[
            "tensorboard_name"], tensorboard["address"],
            color_util.colorize_state(tensorboard[
            "state"]), tensorboard["create_time"], tensorboard[
            "update_time"]))
    else:
      print("{:32} {:32} {:16} {:32} {:32}".format(
          "TENSORBOARD_NAME", "ADDRESS", "STATE", "CREATED", "UPDATED"))
      for tensorboard in response_tensorboard:
        print("{:32} {:32} {:16} {:32} {:32}".format(tensorboard[
            "tensorboard_name"], tensorboard["address"],
            color_util.colorize_state(tensorboard["state"]),
            tensorboard["create_time"], tensorboard["update_time"]))
  else:
    print("response: {}".format(response_tensorboard))


def create_tensorboard_service(args):
  """Create the tensorboard_service."""

  client = CloudMlClient()
  tensorboard = TensorboardService(args.tensorboard_name, args.logdir)

  if args.framework:
    tensorboard.framework = args.framework
  if args.framework_version:
    tensorboard.framework_version = args.framework_version
  if args.docker_image:
    tensorboard.docker_image = args.docker_image
  if args.docker_command:
    tensorboard.docker_command = args.docker_command
  if args.node_selector_key:
    tensorboard.node_selector_key = args.node_selector_key
  if args.node_selector_value:
    tensorboard.node_selector_value = args.node_selector_value

  response = client.create_tensorboard_service(tensorboard)
  if not isinstance(response, str):
    print_tensorboard_info(response)
  else:
    print("response: {}".format(response))


def describe_tensorboard_service(args):
  """Describe the tensorboard_service."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.describe_tensorboard_service(args.tensorboard_name,
                                                   args.org_id)
  else:
    response = client.describe_tensorboard_service(args.tensorboard_name)
  if not isinstance(response, str):
    print_tensorboard_info(response)
  else:
    print("response: {}".format(response))


def delete_tensorboard_service(args):
  """Delete the tensorboard_service."""

  client = CloudMlClient()
  response = client.delete_tensorboard_service(args.tensorboard_name)
  print(response)


def get_tensorboard_service_events(args):
  """Get events of the tensorboard service."""

  client = CloudMlClient()
  response = client.get_tensorboard_service_events(args.tensorboard_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
  else:
    print("response: {}".format(response))


def list_dev_envs(args):
  """List dev environments."""

  client = CloudMlClient()
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_dev_envs = client.list_dev_envs(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_dev_envs = client.list_dev_envs(args.org_id)
  else:
    response_dev_envs = client.list_dev_envs()
  if not isinstance(response_dev_envs, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      print("{:16} {:16} {:32} {:32} {:16} {:32} {:32}".format(
          "ORG ID", "ORG NAME", "DEV_NAME", "ADDRESS", "STATE", "CREATED",
          "UPDATED"))
      for dev_env in response_dev_envs:
        print("{:16} {:16} {:32} {:32} {:16} {:32} {:32}".format(dev_env[
            "org_id"], dev_env["org_name"], dev_env["dev_name"], dev_env[
                "address"], color_util.colorize_state(dev_env["state"]),
                    dev_env["create_time"], dev_env["update_time"]))
    else:
      print("{:32} {:32} {:16} {:32} {:32}".format(
          "DEV_NAME", "ADDRESS", "STATE", "CREATED", "UPDATED"))
      for dev_env in response_dev_envs:
        print("{:32} {:32} {:16} {:32} {:32}".format(dev_env[
            "dev_name"], dev_env["address"],
            color_util.colorize_state(dev_env["state"]), dev_env[
                "create_time"], dev_env["update_time"]))
  else:
    print("response: {}".format(response_dev_envs))


def create_dev_env(args):
  """Create dev env."""

  client = CloudMlClient()
  dev_env = DevEnv(args.dev_name, args.password)

  if args.cpu_limit:
    dev_env.cpu_limit = args.cpu_limit
  if args.memory_limit:
    dev_env.memory_limit = args.memory_limit
  if args.gpu_limit:
    dev_env.gpu_limit = int(args.gpu_limit)
  if args.framework:
    dev_env.framework = args.framework
  if args.framework_version:
    dev_env.framework_version = args.framework_version
  if args.docker_image:
    dev_env.docker_image = args.docker_image
  if args.docker_command:
    dev_env.docker_command = args.docker_command
  if args.node_selector_key:
    dev_env.node_selector_key = args.node_selector_key
  if args.node_selector_value:
    dev_env.node_selector_value = args.node_selector_value
  if args.watch:
    dev_name = args.dev_name

  response_dev_env = client.create_dev_env(dev_env)
  if not isinstance(response_dev_env, str):
    print_dev_env_info(response_dev_env)
    if args.watch:
      print("\nThe dev_env is creating, feel free to Ctrl+C to stop watching\n")
      print("{:32} {:16} {:32} {:32}".format(
              "DEV_NAME",
              "STATE",
              "CREATED",
              "UPDATED"))
      while True:
        watch_response = client.describe_dev_env(dev_name)
        if not isinstance(watch_response, str):
          print("{:32} {:16} {:32} {:32}".format(
                watch_response["dev_name"],
                color_util.colorize_state(watch_response["state"]),
                watch_response["create_time"],
                watch_response["update_time"]))
          if watch_response["state"] == constant.DEV_ENV_STATE_RUNNING:
            return
          try:

            time.sleep(constant.JOB_WATCH_INTERVAL)
          except KeyboardInterrupt:
            return
        else:
          return
  else:
    print("response: {}".format(response_dev_env))


def describe_dev_env(args):
  """Describe the dev environment."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.describe_dev_env(args.dev_name, args.org_id)
  else:
    response = client.describe_dev_env(args.dev_name)
  if not isinstance(response, str):
    print_dev_env_info(response)
  else:
    print("response: {}".format(response))


def delete_dev_env(args):
  """Delete the dev environment."""

  client = CloudMlClient()
  response = client.delete_dev_env(args.dev_name)
  print(response)


def get_dev_env_events(args):
  """Get events of the dev environment."""

  client = CloudMlClient()
  response = client.get_dev_env_events(args.dev_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
  else:
    print("response: {}".format(response))


def get_dev_env_metrics(args):
  """Get the metrics of the dev environment."""

  client = CloudMlClient()
  response = client.get_dev_env_metrics(args.dev_name)
  if not isinstance(response, str):
    print_metrics_result(response)
  else:
    print("response: {}".format(response))


def list_dev_servers(args):
  """List dev servers."""

  client = CloudMlClient()
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_dev_servers = client.list_dev_servers(
          constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_dev_servers = client.list_dev_servers(args.org_id)
  else:
    response_dev_servers = client.list_dev_servers()
  if not isinstance(response_dev_servers, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      print("{:16} {:16} {:32} {:32} {:16} {:32} {:32}".format(
          "ORG ID", "ORG NAME", "DEV_NAME", "ADDRESS", "STATE", "CREATED",
          "UPDATED"))
      for dev_server in response_dev_servers:
        print("{:16} {:16} {:32} {:32} {:16} {:32} {:32}".format(
            dev_server["org_id"], dev_server["org_name"], dev_server[
                "dev_name"], dev_server["address"],
            color_util.colorize_state(dev_server["state"]),
            dev_server["create_time"], dev_server["update_time"]))
    else:
      print("{:32} {:32} {:16} {:32} {:32}".format(
          "DEV_NAME", "ADDRESS", "STATE", "CREATED", "UPDATED"))
      for dev_server in response_dev_servers:
        print("{:32} {:32} {:16} {:32} {:32}".format(
            dev_server["dev_name"], dev_server["address"],
            color_util.colorize_state(dev_server["state"]),
            dev_server["create_time"], dev_server["update_time"]))
  else:
    print("response: {}".format(response_dev_servers))


def create_dev_server(args):
  """Create dev server."""

  client = CloudMlClient()
  dev_server = DevServer(args.dev_name, args.password)

  if args.framework:
    dev_server.framework = args.framework
  if args.framework_version:
    dev_server.framework_version = args.framework_version
  if args.docker_image:
    dev_server.docker_image = args.docker_image
  if args.docker_command:
    dev_server.docker_command = args.docker_command

  response_dev_server = client.create_dev_server(dev_server)
  if not isinstance(response_dev_server, str):
    print_dev_server_info(response_dev_server)
  else:
    print("response: {}".format(response_dev_server))


def describe_dev_server(args):
  """Describe the dev server."""

  client = CloudMlClient()
  if "org_id" in args:
    response = client.describe_dev_server(args.dev_name, args.org_id)
  else:
    response = client.describe_dev_server(args.dev_name)
  if not isinstance(response, str):
    print_dev_server_info(response)
  else:
    print("response: {}".format(response))


def delete_dev_server(args):
  """Delete the dev server."""

  client = CloudMlClient()
  response = client.delete_dev_server(args.dev_name)
  print(response)


def get_dev_server_events(args):
  """Get events of the dev server."""

  client = CloudMlClient()
  response = client.get_dev_server_events(args.dev_name)
  if not isinstance(response, str):
    print_kubernetes_events(response["events"])
  else:
    print("response: {}".format(response))


def list_quota(args):
  """List the quota."""

  client = CloudMlClient()
  if "org_id" in args:
    if args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      response_quotas = client.get_quota(constant.CLOUDML_ALL_ORG_PARAMETER)
    else:
      response_quotas = client.get_quota(args.org_id)
  else:
    response_quotas = client.get_quota()

  if not isinstance(response_quotas, str):
    if "org_id" in args and args.org_id == constant.CLOUDML_ALL_ORG_PARAMETER:
      for quota in response_quotas:
        print("\nThe quota of user {}-{}:".format(quota["org_id"], quota[
            "org_name"]))
        print_quota_info(quota)
    else:
      for quota in response_quotas:
        print_quota_info(quota)
  else:
    print(response_quotas)


def do_predict(args):
  """Do predict."""

  client = CloudMlClient()
  # TODO: Remove duplicated code
  if args.timeout:
    if args.model_version:
      response = client.do_predict(args.model_name, args.model_version,
                                   args.filename, float(args.timeout))
    elif args.server:
      response = client.do_predict_server(args.server, args.model_name,
                                          args.filename, float(args.timeout))
    else:
      print("Need to set either model_version or server, exit now.")
      return 1
  else:
    if args.model_version:
      response = client.do_predict(args.model_name, args.model_version,
                                   args.filename)
    elif args.server:
      response = client.do_predict_server(args.server, args.model_name,
                                          args.filename)
    else:
      print("Need to set either model_version or server, exit now.")
      return 1
  if isinstance(response, str):
    print(response)
  else:
    print_predict_result(response)


def update_job_quota(args):
  client = CloudMlClient()
  quota = Quota(args.org_id, args.org_name)
  if args.cpu:
    quota.train_cpu_quota = args.cpu
  if args.memory:
    quota.train_memory_quota = args.memory
  if args.gpu:
    quota.train_gpu_quota = int(args.gpu)
  if args.count:
    quota.train_count_quota = int(args.count)
  response_quota = client.update_quota(quota)
  if not isinstance(response_quota, str):
    print_quota_info(response_quota)
  else:
    print("response: {}".format(response_quota))


def update_model_quota(args):
  client = CloudMlClient()
  quota = Quota(args.org_id, args.org_name)
  if args.cpu:
    quota.model_cpu_quota = args.cpu
  if args.memory:
    quota.model_memory_quota = args.memory
  if args.gpu:
    quota.model_gpu_quota = int(args.gpu)
  if args.count:
    quota.model_count_quota = int(args.count)
  response_quota = client.update_quota(quota)
  if not isinstance(response_quota, str):
    print_quota_info(response_quota)
  else:
    print("response: {}".format(response_quota))


def update_dev_quota(args):
  client = CloudMlClient()
  quota = Quota(args.org_id, args.org_name)
  if args.cpu:
    quota.dev_cpu_quota = args.cpu
  if args.memory:
    quota.dev_memory_quota = args.memory
  if args.gpu:
    quota.dev_gpu_quota = int(args.gpu)
  if args.count:
    quota.dev_count_quota = int(args.count)
  response_quota = client.update_quota(quota)
  if not isinstance(response_quota, str):
    print_quota_info(response_quota)
  else:
    print("response: {}".format(response_quota))


def update_tensorboard_quota(args):
  client = CloudMlClient()
  quota = Quota(args.org_id, args.org_name)
  if args.tensorboard:
    quota.tensorboard_quota = int(args.tensorboard)
  response_quota = client.update_quota(quota)
  if not isinstance(response_quota, str):
    print_quota_info(response_quota)
  else:
    print("response: {}".format(response_quota))


def update_total_quota(args):
  client = CloudMlClient()
  quota = Quota(args.org_id, args.org_name)
  if args.cpu:
    quota.total_cpu_quota = args.cpu
  if args.memory:
    quota.total_memory_quota = args.memory
  if args.gpu:
    quota.total_gpu_quota = int(args.gpu)
  response_quota = client.update_quota(quota)
  if not isinstance(response_quota, str):
    print_quota_info(response_quota)
  else:
    print("response: {}".format(response_quota))


def update_quota(args):
  if not (args.cpu or args.memory or args.gpu or args.tensorboard or
          args.count):
    print("ERROR: Please give the resource to change")
  else:
    if args.type == "jobs":
      update_job_quota(args)
    elif args.type == "models":
      update_model_quota(args)
    elif args.type == "dev":
      update_dev_quota(args)
    elif args.type == "tensorboard":
      update_tensorboard_quota(args)
    elif args.type == "total":
      update_total_quota(args)
    else:
      print("ERROR: Unknown job type {}".format(args.type))


def list_framework(args):
  """List the framework."""

  client = CloudMlClient()
  response = client.get_frameworks()

  if not isinstance(response, str):
    print_frameworks_info(response)
  else:
    print("response: {}".format(response))


def list_all(args):
  """List all resources."""

  print("List all train jobs:")
  list_jobs(args)
  print("\nList all model services:")
  list_models(args)
  print("\nList all dev environments:")
  list_dev_envs(args)
  print("\nList all tensorboard services:")
  list_tensorboard_services(args)
