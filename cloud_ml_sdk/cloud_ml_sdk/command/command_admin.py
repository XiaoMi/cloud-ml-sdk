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

import argparse
import logging
import sys
sys.path.append("../../")

from . import util

logging.basicConfig(level=logging.DEBUG)


def main():
  parser = argparse.ArgumentParser()
  main_subparser = parser.add_subparsers(dest="command_group", help="Commands")

  # subcommand: jobs
  jobs_parser = main_subparser.add_parser("jobs", help="Commands about jobs")
  jobs_subparser = jobs_parser.add_subparsers(
      dest="job_command", help="Subcommands of jobs")

  # subcommand of jobs: list
  jobs_list_parser = jobs_subparser.add_parser("list", help="List jobs")
  jobs_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  jobs_list_parser.set_defaults(func=util.list_jobs)

  # subcommand of jobs: describe
  jobs_describe_parser = jobs_subparser.add_parser(
      "describe", help="Describe job")
  jobs_describe_parser.add_argument("job_name", help="The name of the job")
  jobs_describe_parser.add_argument(
      "org_id", help="The org_id of the job's owner")
  jobs_describe_parser.set_defaults(func=util.describe_job)

  # subcommand of jobs: logs
  jobs_logs_parser = jobs_subparser.add_parser(
      "logs", help="Get the logs of the job")
  jobs_logs_parser.add_argument("job_name", help="The job to get the logs")
  jobs_logs_parser.add_argument(
      "org_id", help="The org_id of the job's owner")
  jobs_logs_parser.set_defaults(func=util.get_job_logs)

  # subcommand of jobs: events
  jobs_events_parser = jobs_subparser.add_parser(
      "events", help="Get the events of the train job")
  jobs_events_parser.add_argument("job_name", help="The name of the train job")
  jobs_events_parser.add_argument(
      "org_id", help="The org_id of the job's owner")
  jobs_events_parser.set_defaults(func=util.get_train_job_events)

  # subcommand: model
  models_parser = main_subparser.add_parser(
      "models", help="Commands about models")
  models_subparser = models_parser.add_subparsers(
      dest="model_command", help="Subcommands of models")

  # subcommand of models: list
  models_list_parser = models_subparser.add_parser("list", help="List models")
  models_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  models_list_parser.set_defaults(func=util.list_models)

  # subcommand of models: describe
  models_describe_parser = models_subparser.add_parser(
      "describe", help="Describe model")
  models_describe_parser.add_argument(
      "model_name", help="The name of the model")
  models_describe_parser.add_argument(
      "model_version", help="The version of the model")
  models_describe_parser.add_argument(
      "org_id", help="The org_id of the model's owner")
  models_describe_parser.set_defaults(func=util.describe_model)

  # subcommand of models: logs
  models_logs_parser = models_subparser.add_parser(
      "logs", help="Get the logs of the model service")
  models_logs_parser.add_argument("model_name", help="The name of the model")
  models_logs_parser.add_argument(
      "model_version", help="The version of the model")
  models_logs_parser.add_argument(
      "org_id", help="The org_id of the model's owner")
  models_logs_parser.set_defaults(func=util.get_model_logs)

  # subcommand of models: events
  models_events_parser = models_subparser.add_parser(
      "events", help="Get the events of the model service")
  models_events_parser.add_argument(
      "model_name", help="The name of the model service")
  models_events_parser.add_argument(
      "model_version", help="The version of the model service")
  models_events_parser.add_argument(
      "org_id", help="The org_id of the model's owner")
  models_events_parser.set_defaults(func=util.get_model_service_events)

  # subcommand: dev
  dev_parser = main_subparser.add_parser("dev", help="Commands about dev")
  dev_subparser = dev_parser.add_subparsers(
      dest="dev_command", help="Subcommands of dev")

  # subcommand of dev: list
  dev_list_parser = dev_subparser.add_parser("list", help="List devs")
  dev_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  dev_list_parser.set_defaults(func=util.list_dev_envs)

  # subcommand of dev: describe
  dev_describe_parser = dev_subparser.add_parser(
      "describe", help="Describe dev")
  dev_describe_parser.add_argument("dev_name", help="The name of the dev")
  dev_describe_parser.add_argument(
      "org_id", help="The org_id of the dev's owner")
  dev_describe_parser.set_defaults(func=util.describe_dev_env)

  # subcommand: dev_server
  dev_server_parser = main_subparser.add_parser(
      "dev_server", help="Commands about dev_server")
  dev_server_subparser = dev_server_parser.add_subparsers(
      dest="dev_server_command", help="Subcommands of dev_server")

  # subcommand of dev_server: list
  dev_server_list_parser = dev_server_subparser.add_parser(
      "list", help="List dev_servers")
  dev_server_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  dev_server_list_parser.set_defaults(func=util.list_dev_servers)

  # subcommand of dev_server: describe
  dev_server_describe_parser = dev_server_subparser.add_parser(
      "describe", help="Describe dev_server")
  dev_server_describe_parser.add_argument(
      "dev_name", help="The name of the dev_server")
  dev_server_describe_parser.add_argument(
      "org_id", help="The org_id of the dev_server's owner")
  dev_server_describe_parser.set_defaults(func=util.describe_dev_server)

  # subcommand: tensorboard
  tensorboard_parser = main_subparser.add_parser(
      "tensorboard", help="Commands about tensorboard")
  tensorboard_subparser = tensorboard_parser.add_subparsers(
      dest="tensorboard_command", help="Subcommands of tensorboard")

  # subcommand of tensorboard: list
  tensorboard_list_parser = tensorboard_subparser.add_parser(
      "list", help="List tensorboard")
  tensorboard_list_parser.add_argument(
      "org_id", help="The org_id to list (with -1 stand for all)")
  tensorboard_list_parser.set_defaults(func=util.list_tensorboard_services)

  # subcommand of tensorboard: describe
  tensorboard_describe_parser = tensorboard_subparser.add_parser(
      "describe", help="Describe tensorboard")
  tensorboard_describe_parser.add_argument(
      "tensorboard_name", help="The name of the tensorboard")
  tensorboard_describe_parser.add_argument(
      "org_id", help="The org_id of the tensorboard's owner")
  tensorboard_describe_parser.set_defaults(
      func=util.describe_tensorboard_service)

  # subcommand: quota
  quota_parser = main_subparser.add_parser(
      "quota", help="Commands about quota")
  quota_subparser = quota_parser.add_subparsers(
      dest="quota_command", help="Subcommands of quota")

  # subcommand of quota: list
  quota_list_parser = quota_subparser.add_parser("list", help="List the quota")
  quota_list_parser.add_argument(
      "org_id", help="Org_id to list (with -1 stand for all)")
  quota_list_parser.set_defaults(func=util.list_quota)

  # subcommand of quota: update
  quota_update_parser = quota_subparser.add_parser(
      "update", help="Update quota")
  quota_update_parser.add_argument("org_id", help="The org_id to set")
  quota_update_parser.add_argument(
      "-n", "--org_name", dest="org_name", help="The org_name to set")
  quota_update_parser.add_argument(
      "-t",
      "--type",
      dest="type",
      help="The job type to update, support for jobs, models, dev, tensorboard, total",
      required=True)
  quota_update_parser.add_argument(
      "-c", "--cpu", dest="cpu", help="The new cpu quota")
  quota_update_parser.add_argument(
      "-m", "--memory", dest="memory", help="The new memory quota")
  quota_update_parser.add_argument(
      "-g", "--gpu", dest="gpu", help="The new gpu quota")
  quota_update_parser.add_argument(
      "-T",
      "--tensorboard",
      dest="tensorboard",
      help="The new tensorboard quota")
  quota_update_parser.add_argument(
      "-C", "--count", dest="count", help="The count quota")
  quota_update_parser.set_defaults(func=util.update_quota)

  args = parser.parse_args()
  args.func(args)


if __name__ == "__main__":
  main()
