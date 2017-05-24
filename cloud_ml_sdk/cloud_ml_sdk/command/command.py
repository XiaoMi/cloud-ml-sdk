#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

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

import argcomplete
import argparse
import logging
import pkg_resources
import sys
sys.path.append("../../")

from . import constant
from . import util

logging.basicConfig(level=logging.DEBUG)


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument(
      "-v",
      "--version",
      action="version",
      version=pkg_resources.require(constant.SDK_NAME)[0].version,
      help="Show version")

  main_subparser = parser.add_subparsers(dest="command_group", help="Commands")

  init_parser = main_subparser.add_parser("init", help="Init cloudml config")
  init_parser.set_defaults(func=util.init_config)

  org_id_parser = main_subparser.add_parser(
      "org_id", help="Get org_id by access_key and secret_key")
  org_id_parser.set_defaults(func=util.get_org_id)

  # subcommand: jobs
  jobs_parser = main_subparser.add_parser("jobs", help="Commands about jobs")
  jobs_subparser = jobs_parser.add_subparsers(
      dest="job_command", help="Subcommands of jobs")

  # subcommand of jobs: list
  jobs_list_parser = jobs_subparser.add_parser("list", help="List jobs")
  jobs_list_parser.set_defaults(func=util.list_jobs)

  # subcommand of jobs: submit
  jobs_submit_parser = jobs_subparser.add_parser("submit", help="Submit job")
  jobs_submit_parser.add_argument(
      "-f",
      "--filename",
      dest="filename",
      help="The json file contains the job task msg")
  jobs_submit_parser.add_argument(
      "-n", "--job_name", dest="job_name", help="The job name")
  jobs_submit_parser.add_argument(
      "-m", "--module_name", dest="module_name", help="The module name")
  jobs_submit_parser.add_argument(
      "-u", "--trainer_uri", dest="trainer_uri", help="The trainer uri")
  jobs_submit_parser.add_argument(
      "-a", "--job_args", dest="job_args", help="The string of args")
  jobs_submit_parser.add_argument(
      "-c",
      "--cpu_limit",
      dest="cpu_limit",
      help="The CPU limit with unit core")
  jobs_submit_parser.add_argument(
      "-M",
      "--memory_limit",
      dest="memory_limit",
      help="The memory limit with unit K, M or G")
  jobs_submit_parser.add_argument(
      "-g", "--gpu_limit", dest="gpu_limit", help="The number of GPU limit")
  jobs_submit_parser.add_argument(
      "-p",
      "--ps_count",
      dest="ps_count",
      help="The number of ps for distributed training")
  jobs_submit_parser.add_argument(
      "-w",
      "--worker_count",
      dest="worker_count",
      help="The number of worker for distributed training")
  jobs_submit_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The docker image")
  jobs_submit_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  jobs_submit_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  jobs_submit_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  jobs_submit_parser.add_argument(
      "-vt", "--volume_type", dest="volume_type", help="The volume type")
  jobs_submit_parser.add_argument(
      "-vp", "--volume_path", dest="volume_path", help="The volume path")
  jobs_submit_parser.add_argument(
      "-mp", "--mount_path", dest="mount_path", help="The mount type")
  jobs_submit_parser.add_argument(
      "-mro",
      "--mount_read_only",
      dest="mount_read_only",
      help="Whether mount read only or not")
  jobs_submit_parser.add_argument(
      "-pc",
      "--prepare_command",
      dest="prepare_command",
      help="The prepare command")
  jobs_submit_parser.add_argument(
      "-fc",
      "--finish_command",
      dest="finish_command",
      help="The finish command")
  jobs_submit_parser.add_argument(
      "-W", "--watch", action="store_true", help="Watch the status of job")
  jobs_submit_parser.add_argument(
      "-nsk",
      "--node_selector_key",
      dest="node_selector_key",
      help="The node selector key")
  jobs_submit_parser.add_argument(
      "-nsv",
      "--node_selector_value",
      dest="node_selector_value",
      help="The node selector value")

  jobs_submit_parser.set_defaults(func=util.submit_job)

  # subcommand of jobs: describe
  jobs_describe_parser = jobs_subparser.add_parser(
      "describe", help="Describe job")
  jobs_describe_parser.add_argument("job_name", help="The job to describe")
  jobs_describe_parser.set_defaults(func=util.describe_job)

  # subcommand of jobs: logs
  jobs_logs_parser = jobs_subparser.add_parser(
      "logs", help="Get the logs of the job")
  jobs_logs_parser.add_argument("job_name", help="The job to get the logs")
  jobs_logs_parser.set_defaults(func=util.get_job_logs)

  # subcommand of jobs: metrics
  jobs_metrics_parser = jobs_subparser.add_parser(
      "metrics", help="Get the metrics of the job")
  jobs_metrics_parser.add_argument("job_name", help="The job to get the logs")
  jobs_metrics_parser.set_defaults(func=util.get_job_metrics)

  # subcommand of jobs: hp
  jobs_hp_parser = jobs_subparser.add_parser(
      "hp", help="Get the hyperparameters data of the job")
  jobs_hp_parser.add_argument("job_name", help="The job name")
  jobs_hp_parser.set_defaults(func=util.get_job_hyperparameters_data)

  # subcommand of jobs: delete
  jobs_delete_parser = jobs_subparser.add_parser(
      "delete", help="Delete the job")
  jobs_delete_parser.add_argument("job_name", help="The name of the job")
  jobs_delete_parser.set_defaults(func=util.delete_job)

  # subcommand of jobs: events
  jobs_events_parser = jobs_subparser.add_parser(
      "events", help="Get the events of the train job")
  jobs_events_parser.add_argument("job_name", help="The name of the train job")
  jobs_events_parser.set_defaults(func=util.get_train_job_events)

  # subcommand: models
  models_parser = main_subparser.add_parser(
      "models", help="Commands about models")
  models_subparser = models_parser.add_subparsers(
      dest="models_command", help="Subcommands of models")

  # subcommand of models: list
  models_list_parser = models_subparser.add_parser(
      "list", help="List model services")
  models_list_parser.set_defaults(func=util.list_models)

  # subcommand of models: create
  models_create_parser = models_subparser.add_parser(
      "create", help="Create model service")
  models_create_parser.add_argument(
      "-n",
      "--model_name",
      dest="model_name",
      help="The name of the model",
      required=True)
  models_create_parser.add_argument(
      "-v",
      "--model_version",
      dest="model_version",
      help="The version of the model",
      required=True)
  models_create_parser.add_argument(
      "-u",
      "--model_uri",
      dest="model_uri",
      help="The uri of the model",
      required=True)
  models_create_parser.add_argument(
      "-a", "--model_args", dest="model_args", help="The string of args")
  models_create_parser.add_argument(
      "-c",
      "--cpu_limit",
      dest="cpu_limit",
      help="The CPU limit with unit core")
  models_create_parser.add_argument(
      "-M",
      "--memory_limit",
      dest="memory_limit",
      help="The memory limit with unit K, M or G")
  models_create_parser.add_argument(
      "-g", "--gpu_limit", dest="gpu_limit", help="The number of GPU limit")
  models_create_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The docker image")
  models_create_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  models_create_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  models_create_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  models_create_parser.add_argument(
      "-r", "--replicas", dest="replicas", help="The num of replicas")
  models_create_parser.add_argument(
      "-pc",
      "--prepare_command",
      dest="prepare_command",
      help="The prepare command")
  models_create_parser.add_argument(
      "-fc",
      "--finish_command",
      dest="finish_command",
      help="The finish command")
  models_create_parser.add_argument(
      "-nsk",
      "--node_selector_key",
      dest="node_selector_key",
      help="The node selector key")
  models_create_parser.add_argument(
      "-nsv",
      "--node_selector_value",
      dest="node_selector_value",
      help="The node selector value")
  models_create_parser.add_argument(
      "-W", "--watch", action="store_true", help="Watch the status of model creation")

  models_create_parser.set_defaults(func=util.create_model)

  # subcommand of models: describe
  models_describe_parser = models_subparser.add_parser(
      "describe", help="Describe the model service")
  models_describe_parser.add_argument(
      "model_name", help="The name of the model")
  models_describe_parser.add_argument(
      "model_version", help="The version of the model")
  models_describe_parser.set_defaults(func=util.describe_model)

  # subcommand of models: update
  models_update_parser = models_subparser.add_parser(
      "update", help="Update the model service")
  models_update_parser.add_argument(
      "model_name", help="The name of the model")
  models_update_parser.add_argument(
      "model_version", help="The version of the model")
  models_update_parser.add_argument(
      "-r", "--replicas", dest="replicas", help="The num of replicas")
  models_update_parser.set_defaults(func=util.update_model)

  # subcommand of models: logs
  models_logs_parser = models_subparser.add_parser(
      "logs", help="Get the logs of the model service")
  models_logs_parser.add_argument("model_name", help="The name of the model")
  models_logs_parser.add_argument(
      "model_version", help="The version of the model")
  models_logs_parser.set_defaults(func=util.get_model_logs)

  # subcommand of models: metrics
  models_metrics_parser = models_subparser.add_parser(
      "metrics", help="Get the metrics of the model service")
  models_metrics_parser.add_argument("model_name", help="The name of the model")
  models_metrics_parser.add_argument(
      "model_version", help="The version of the model")
  models_metrics_parser.set_defaults(func=util.get_model_metrics)

  # subcommand of models: delete
  models_delete_parser = models_subparser.add_parser(
      "delete", help="Delete the model service")
  models_delete_parser.add_argument("model_name", help="The name of the model")
  models_delete_parser.add_argument(
      "model_version", help="The version of the model")
  models_delete_parser.set_defaults(func=util.delete_model)

  # subcommand of models: predict
  models_predict_parser = models_subparser.add_parser(
      "predict", help="Request the model service and predict")
  models_predict_parser.add_argument(
      "-n",
      "--model_name",
      dest="model_name",
      help="The name of the model",
      required=True)
  models_predict_parser.add_argument(
      "-v",
      "--model_version",
      dest="model_version",
      help="The version of the model")
  models_predict_parser.add_argument(
      "-s", "--server", dest="server", help="The address of the server")
  models_predict_parser.add_argument(
      "-f",
      "--filename",
      dest="filename",
      help="The json data file",
      required=True)
  models_predict_parser.add_argument(
      "-t", "--timeout", dest="timeout", help="The timeout of gRPC request")
  models_predict_parser.set_defaults(func=util.do_predict)

  # subcommand of models: events
  models_events_parser = models_subparser.add_parser(
      "events", help="Get the events of the model service")
  models_events_parser.add_argument(
      "model_name", help="The name of the model service")
  models_events_parser.add_argument(
      "model_version", help="The version of the model service")
  models_events_parser.set_defaults(func=util.get_model_service_events)

  # subcommand: tensorboard
  tensorboard_parser = main_subparser.add_parser(
      "tensorboard", help="Commands about tensorboard")
  tensorboard_subparser = tensorboard_parser.add_subparsers(
      dest="tensorboard_command", help="Subcommands of tensorboard")

  # subcommand of tensorboard: list
  tensorboard_list_parser = tensorboard_subparser.add_parser(
      "list", help="List tensorboards")
  tensorboard_list_parser.set_defaults(func=util.list_tensorboard_services)

  # subcommand of tensorboard: create
  tensorboard_create_parser = tensorboard_subparser.add_parser(
      "create", help="Create tensorboard")
  tensorboard_create_parser.add_argument(
      "-n",
      "--tensorboard_name",
      dest="tensorboard_name",
      help="The name of the tensorboard",
      required=True)
  tensorboard_create_parser.add_argument(
      "-l",
      "--logdir",
      dest="logdir",
      help="The directory of tensorboard log",
      required=True)
  tensorboard_create_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The docker image")
  tensorboard_create_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  tensorboard_create_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  tensorboard_create_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  tensorboard_create_parser.add_argument(
      "-nsk",
      "--node_selector_key",
      dest="node_selector_key",
      help="The node selector key")
  tensorboard_create_parser.add_argument(
      "-nsv",
      "--node_selector_value",
      dest="node_selector_value",
      help="The node selector value")

  tensorboard_create_parser.set_defaults(func=util.create_tensorboard_service)

  # subcommand of tensorboard: describe
  tensorboard_describe_parser = tensorboard_subparser.add_parser(
      "describe", help="Describe the tensorboard")
  tensorboard_describe_parser.add_argument(
      "tensorboard_name", help="The name of the tensorboard")
  tensorboard_describe_parser.set_defaults(
      func=util.describe_tensorboard_service)

  # subcommand of tensorboard: delete
  tensorboard_delete_parser = tensorboard_subparser.add_parser(
      "delete", help="Delete the tensorboard")
  tensorboard_delete_parser.add_argument(
      "tensorboard_name", help="The name of the tensorboard")
  tensorboard_delete_parser.set_defaults(func=util.delete_tensorboard_service)

  # subcommand of tensorboard: events
  tensorboard_events_parser = tensorboard_subparser.add_parser(
      "events", help="Get the events of the tensorboard service")
  tensorboard_events_parser.add_argument(
      "tensorboard_name", help="The name of the tensorboard service")
  tensorboard_events_parser.set_defaults(
      func=util.get_tensorboard_service_events)

  # subcommand: dev
  dev_parser = main_subparser.add_parser("dev", help="Commands about dev")
  dev_subparser = dev_parser.add_subparsers(
      dest="dev_command", help="Subcommands of dev")

  # subcommand of dev: list
  dev_list_parser = dev_subparser.add_parser(
      "list", help="List dev environments")
  dev_list_parser.set_defaults(func=util.list_dev_envs)

  # subcommand of dev: create
  dev_create_parser = dev_subparser.add_parser(
      "create", help="Create dev environment")
  dev_create_parser.add_argument(
      "-n",
      "--dev_name",
      dest="dev_name",
      help="The dev environment name",
      required=True)
  dev_create_parser.add_argument(
      "-p",
      "--password",
      dest="password",
      help="The password of ipython notebook",
      required=True)
  dev_create_parser.add_argument(
      "-c",
      "--cpu_limit",
      dest="cpu_limit",
      help="The CPU limit with unit core")
  dev_create_parser.add_argument(
      "-M",
      "--memory_limit",
      dest="memory_limit",
      help="The memory limit with unit K, M or G")
  dev_create_parser.add_argument(
      "-g", "--gpu_limit", dest="gpu_limit", help="The number of GPU limit")
  dev_create_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The ")
  dev_create_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  dev_create_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  dev_create_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  dev_create_parser.add_argument(
      "-nsk",
      "--node_selector_key",
      dest="node_selector_key",
      help="The node selector key")
  dev_create_parser.add_argument(
      "-nsv",
      "--node_selector_value",
      dest="node_selector_value",
      help="The node selector value")
  dev_create_parser.add_argument(
    "-W", "--watch", action="store_true", help="Watch the status of dev_env creation")

  dev_create_parser.set_defaults(func=util.create_dev_env)

  # subcommand of dev: describe
  dev_describe_parser = dev_subparser.add_parser(
      "describe", help="Describe the dev environment")
  dev_describe_parser.add_argument(
      "dev_name", help="The name of dev environment")
  dev_describe_parser.set_defaults(func=util.describe_dev_env)

  # subcommand of dev: delete
  dev_delete_parser = dev_subparser.add_parser(
      "delete", help="Delete the dev environment")
  dev_delete_parser.add_argument(
      "dev_name", help="The name of dev environment")
  dev_delete_parser.set_defaults(func=util.delete_dev_env)

  # subcommand of dev: events
  dev_events_parser = dev_subparser.add_parser(
      "events", help="Get the events of the dev environment")
  dev_events_parser.add_argument(
      "dev_name", help="The name of dev environment")
  dev_events_parser.set_defaults(func=util.get_dev_env_events)

  # subcommand of dev: metrics
  dev_metrics_parser = dev_subparser.add_parser(
      "metrics", help="Get the metrics of the dev environment")
  dev_metrics_parser.add_argument(
      "dev_name", help="The name of dev environment")
  dev_metrics_parser.set_defaults(func=util.get_dev_env_metrics)

  # subcommand: dev_server
  dev_server_parser = main_subparser.add_parser(
      "dev_server", help="Commands about dev_server")
  dev_server_subparser = dev_server_parser.add_subparsers(
      dest="dev_server_command", help="Subcommands of dev_server")

  # subcommand of dev_server: list
  dev_server_list_parser = dev_server_subparser.add_parser(
      "list", help="List dev servers")
  dev_server_list_parser.set_defaults(func=util.list_dev_servers)

  # subcommand of dev_server: create
  dev_server_create_parser = dev_server_subparser.add_parser(
      "create", help="Create dev server")
  dev_server_create_parser.add_argument(
      "-n",
      "--dev_name",
      dest="dev_name",
      help="The dev environment name",
      required=True)
  dev_server_create_parser.add_argument(
      "-p",
      "--password",
      dest="password",
      help="The password of ipython notebook",
      required=True)
  dev_server_create_parser.add_argument(
      "-d", "--docker_image", dest="docker_image", help="The ")
  dev_server_create_parser.add_argument(
      "-dc",
      "--docker_command",
      dest="docker_command",
      help="The docker command")
  dev_server_create_parser.add_argument(
      "-F",
      "--framework",
      dest="framework",
      help="The framework of machine learning")
  dev_server_create_parser.add_argument(
      "-V",
      "--framework_version",
      dest="framework_version",
      help="The version of the framework")
  dev_server_create_parser.set_defaults(func=util.create_dev_server)

  # subcommand of dev_server: describe
  dev_server_describe_parser = dev_server_subparser.add_parser(
      "describe", help="Describe the dev server")
  dev_server_describe_parser.add_argument(
      "dev_name", help="The name of dev server")
  dev_server_describe_parser.set_defaults(func=util.describe_dev_server)

  # subcommand of dev_server: delete
  dev_server_delete_parser = dev_server_subparser.add_parser(
      "delete", help="Delete the dev server")
  dev_server_delete_parser.add_argument(
      "dev_name", help="The name of dev server")
  dev_server_delete_parser.set_defaults(func=util.delete_dev_server)

  # subcommand of dev_server: events
  dev_server_events_parser = dev_server_subparser.add_parser(
      "events", help="Get the events of the dev server")
  dev_server_events_parser.add_argument(
      "dev_name", help="The name of dev server")
  dev_server_events_parser.set_defaults(func=util.get_dev_server_events)

  # subcommand: quota
  quota_parser = main_subparser.add_parser(
      "quota", help="Commands about quota")
  quota_subparser = quota_parser.add_subparsers(
      dest="quota_command", help="Subcommands of quota")

  # subcommand of quota: list
  quota_list_parser = quota_subparser.add_parser("list", help="List the quota")
  quota_list_parser.set_defaults(func=util.list_quota)

  # subcommand: framework
  framework_parser = main_subparser.add_parser(
      "framework", help="Commands about framework")
  framework_subparser = framework_parser.add_subparsers(
      dest="framework_command", help="Subcommands of framework")

  # subcommand of framework: list
  framework_list_parser = framework_subparser.add_parser(
      "list", help="List the frameworks")
  framework_list_parser.set_defaults(func=util.list_framework)

  # subcommand: all
  all_parser = main_subparser.add_parser(
      "all", help="Commands about all")
  all_subparser = all_parser.add_subparsers(
      dest="all_command", help="Subcommands of all")

  # subcommand of all: list
  all_list_parser = all_subparser.add_parser(
      "list", help="List all resources")
  all_list_parser.set_defaults(func=util.list_all)

  # For auto-complete
  argcomplete.autocomplete(parser)

  if len(sys.argv) == 1:
    args = parser.parse_args(["-h"])
  else:
    args = parser.parse_args(sys.argv[1:])
  args.func(args)


if __name__ == "__main__":
  main()
