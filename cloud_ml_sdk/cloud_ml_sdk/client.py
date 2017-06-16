# -*- coding: utf-8 -*-

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
import requests
import sys

from cloud_ml_common.auth.signature import Signer

sys.path.append("../../cloud_ml_common/")
logging.basicConfig(level=logging.DEBUG)


class CloudMlClient(object):
  """The client to auth and operate to cloud-ml.

  A CloudMlClient instance authentic the user identity as it is created.
  And a client can handle cloud-ml job)
   methods.
  """

  def __init__(self, access_key=None, secret_key=None, endpoint=None):
    """Create a new CloudMlClient with given definition.

    The `access_key` and `secret_key` must be provided.

    Args:
      access_key: Access key for authentic.
      secret_key: Secret key for authentic.
    """
    if access_key == None or secret_key == None:
      # TODO: check and catch exception
      # Get keys from environment variables
      if "XIAOMI_ACCESS_KEY_ID" in os.environ and "XIAOMI_SECRET_ACCESS_KEY" in os.environ:
        access_key = os.environ["XIAOMI_ACCESS_KEY_ID"]
        secret_key = os.environ["XIAOMI_SECRET_ACCESS_KEY"]
      else:
        # Read keys from configuration file
        config_filename = os.path.join(
            os.path.expanduser("~"), ".config/xiaomi/config")
        if os.path.exists(config_filename):
          try:
            with open(config_filename) as f:
              data = json.load(f)
              access_key = data["xiaomi_access_key_id"]
              secret_key = data["xiaomi_secret_access_key"]
          except Exception as e:
            raise ValueError(
                "Failed to load config data, is the json data in right format? Exception content: {}".format(
                    e))
        else:
          raise StandardError(
              "Can't find access key and secret key, please run cloudml init")

    if endpoint == None:
      self._endpoint = ""
      if "XIAOMI_CLOUDML_ENDPOINT" in os.environ:
        self._endpoint = os.environ["XIAOMI_CLOUDML_ENDPOINT"]
      else:
        config_filename = os.path.join(
            os.path.expanduser("~"), ".config/xiaomi/config")
        if os.path.exists(config_filename):
          with open(config_filename) as f:
            data = json.load(f)
            self._endpoint = data["xiaomi_cloudml_endpoint"]
        else:
          raise StandardError(
              "Can't find cloudml endpoint, please run cloudml init")
    else:
      self._endpoint = endpoint

    self._auth = Signer(access_key, secret_key)
    self._train_url = self._endpoint + "/cloud_ml/v1/train"
    self._model_url = self._endpoint + "/cloud_ml/v1/model"
    self._dev_url = self._endpoint + "/cloud_ml/v1/dev"
    self._tensorboard_url = self._endpoint + "/cloud_ml/v1/tensorboard"
    self._quota_url = self._endpoint + "/cloud_ml/v1/quota"
    self._framework_url = self._endpoint + "/cloud_ml/v1/framework"
    self._authentication_url = self._endpoint + "/cloud_ml/v1/authentication"
    self._org_id_url = self._endpoint + "/cloud_ml/v1/org_ids"
    self._dev_server_url = self._endpoint + "/dev_server/v1/dev_servers"

  @property
  def endpoint(self):
    return self._endpoint

  @endpoint.setter
  def endpoint(self, value):
    """Function for setting endpoint.

    Args:
      value: String value that is going to be set to endpoint. Which must
             start with `http://`.

    Raises:
      ValueError: If value is not str type or not starts with `http://`.
    """
    if not isinstance(value, str):
      raise ValueError("endpoint must be a string!")
    if not value.startswith("http://"):
      raise ValueError("endpoint must start with `http://`!")
    self._endpoint = value
    self._train_url = self._endpoint + "/cloud_ml/v1/train"
    self._model_url = self._endpoint + "/cloud_ml/v1/model"
    self._dev_url = self._endpoint + "/cloud_ml/v1/dev"
    self._tensorboard_url = self._endpoint + "/cloud_ml/v1/tensorboard"
    self._quota_url = self._endpoint + "/cloud_ml/v1/quota"
    self._framework_url = self._endpoint + "/cloud_ml/v1/framework"
    self._authentication_url = self._endpoint + "/cloud_ml/v1/authentication"
    self._org_id_url = self._endpoint + "/cloud_ml/v1/org_ids"
    self._dev_server_url = self._endpoint + "/dev_server/v1/dev_servers"

  def submit_train_job(self, json_data):
    """Submit a train_job to run.

    Args:
      json_data: The json data of train job to submit.

    Returns:
      The dictionary of train job.
    """
    response = requests.post(self._train_url, auth=self._auth, data=json_data)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def list_train_jobs(self, org_id=None):
    """List train jobs.

    Args:
      The org_id whose train_jobs to list.

    Returns:
      The list of dictionary of train jobs.
    """
    if org_id:
      url = self._train_url + "?org_id=" + org_id
    else:
      url = self._train_url
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))["data"]
    else:
      return response.content

  def describe_train_job(self, job_name, org_id=None):
    """Describe and get information of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The dictionary of train job.
    """
    if org_id:
      url = self._train_url + "/" + job_name + "?org_id=" + org_id
    else:
      url = self._train_url + "/" + job_name
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_train_job_logs(self, job_name, org_id=None):
    """Get logs of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The logs of train job.
    """
    if org_id:
      url = self._train_url + "/" + job_name + "/logs" + "?org_id=" + org_id
    else:
      url = self._train_url + "/" + job_name + "/logs"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_train_job_metrics(self, job_name, org_id=None):
    """Get the metrics of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The logs of train job.
    """
    if org_id:
      url = self._train_url + "/" + job_name + "/metrics" + "?org_id=" + org_id
    else:
      url = self._train_url + "/" + job_name + "/metrics"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_train_job_hyperparameters_data(self, job_name):
    """Get hyperparameters data of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The hyperparameter data of train job.
    """
    url = self._train_url + "/" + job_name + "/hyperparameters"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def delete_train_job(self, job_name):
    """Delete the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The response.
    """
    url = self._train_url + "/" + job_name
    response = requests.delete(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_train_job_events(self, job_name, org_id=None):
    """Get events of the train job.

    Args:
      job_name: The name of the train job.

    Returns:
      The events of the train job.
    """
    if org_id:
      url = self._train_url + "/" + job_name + "/events" +  "?org_id=" + org_id
    else:
      url = self._train_url + "/" + job_name + "/events"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def create_model_service(self, model_service):
    """Create the model service.

    Args:
      model_service: The model service object to create.

    Returns:
      The dictionary of model service.
    """
    model_service_data = model_service.get_json_data()
    response = requests.post(self._model_url,
                             auth=self._auth,
                             data=model_service_data)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def list_model_services(self, org_id=None):
    """List model services.

    Returns:
      The list of dictionary of model services.
    """
    if org_id:
      url = self._model_url + "?org_id=" + org_id
    else:
      url = self._model_url
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))["data"]
    else:
      return response.content

  def describe_model_service(self, model_name, model_version, org_id=None):
    """Describe and get information of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The dictionary of model service.
    """
    if org_id:
      url = self._model_url + "/" + model_name + "/" + model_version + "?org_id=" + org_id
    else:
      url = self._model_url + "/" + model_name + "/" + model_version
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def update_model_service(self, model_name, model_version, update_json, org_id=None):
    """Describe and get information of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.
      update_json: The json data to update the model service.

    Returns:
      The dictionary of model service.
    """
    if org_id:
      url = self._model_url + "/" + model_name + "/" + model_version + "?org_id=" + org_id
    else:
      url = self._model_url + "/" + model_name + "/" + model_version
    response = requests.put(url, auth=self._auth, data=update_json)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_model_service_logs(self, model_name, model_version, org_id=None, replica_index=None):
    """Get logs of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.
      org_id: the client's orgid
      replica_index: the replica's index, 

    Returns:
      The logs of the model service.
    """
    if org_id:
      if replica_index:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs" + "?org_id=" + org_id + \
              "&replica=" + replica_index
      else:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs" + "?org_id=" + org_id
    else:
      if replica_index:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs" + "?replica=" + replica_index
      else:
        url = self._model_url + "/" + model_name + "/" + model_version + "/logs"

    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_model_service_metrics(self, model_name, model_version, org_id=None):
    """Get the metrics of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The logs of the model service.
    """
    if org_id:
      url = self._model_url + "/" + model_name + "/" + model_version + "/metrics" + "?org_id=" + org_id
    else:
      url = self._model_url + "/" + model_name + "/" + model_version + "/metrics"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def delete_model_service(self, model_name, model_version):
    """Delete the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The response.
    """
    url = self._model_url + "/" + model_name + "/" + model_version
    response = requests.delete(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_model_service_events(self, model_name, model_version, org_id=None):
    """Get events of the model service.

    Args:
      model_name: The name of the model service.
      model_version: The version of the model service.

    Returns:
      The events of the model service.
    """
    if org_id:
      url = self._model_url + "/" + model_name + "/" + model_version + "/events" + "?org_id=" + org_id
    else:
      url = self._model_url + "/" + model_name + "/" + model_version + "/events"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def create_dev_env(self, dev_env):
    """Create the dev env.

    Args:
      dev_env: The dev env object to submit.

    Returns:
      The dictionary of dev env.
    """
    dev_env_data = dev_env.get_json_data()
    response = requests.post(self._dev_url, auth=self._auth, data=dev_env_data)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def list_dev_envs(self, org_id=None):
    """List the dev environments.

    Returns:
      The list of dictionary of dev env.
    """
    if org_id:
      url = self._dev_url + "?org_id=" + org_id
    else:
      url = self._dev_url
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))["data"]
    else:
      return response.content

  def describe_dev_env(self, dev_name, org_id=None):
    """Describe and get information of the dev environment.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The dictionary of dev environment.
    """
    if org_id:
      url = self._dev_url + "/" + dev_name + "?org_id=" + org_id
    else:
      url = self._dev_url + "/" + dev_name
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def delete_dev_env(self, dev_name):
    """Delete the dev environment.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The response.
    """
    url = self._dev_url + "/" + dev_name
    response = requests.delete(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_dev_env_events(self, dev_name):
    """Get events of the dev env.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The events of the dev env.
    """
    url = self._dev_url + "/" + dev_name + "/events"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_dev_env_metrics(self, dev_name):
    """Get the metrics of the dev env.

    Args:
      dev_name: The name of the dev environment.

    Returns:
      The events of the dev env.
    """
    url = self._dev_url + "/" + dev_name + "/metrics"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def create_dev_server(self, dev_server):
    """Create the dev server.

    Args:
      dev_server: The dev server object to submit.

    Returns:
      The dictionary of dev server.
    """
    dev_server_data = dev_server.get_json_data()
    response = requests.post(self._dev_server_url,
                             auth=self._auth,
                             data=dev_server_data)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def list_dev_servers(self, org_id=None):
    """List the dev servers.

    Returns:
      The list of dictionary of dev server.
    """
    if org_id:
      url = self._dev_server_url + "?org_id=" + org_id
    else:
      url = self._dev_server_url
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))["data"]
    else:
      return response.content

  def describe_dev_server(self, dev_name, org_id=None):
    """Describe and get information of the dev server.

    Args:
      dev_name: The name of the dev server.

    Returns:
      The dictionary of dev server.
    """
    if org_id:
      url = self._dev_server_url + "/" + dev_name + "?org_id=" + org_id
    else:
      url = self._dev_server_url + "/" + dev_name
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def delete_dev_server(self, dev_name):
    """Delete the dev server.

    Args:
      dev_name: The name of the dev server.

    Returns:
      The response.
    """
    url = self._dev_server_url + "/" + dev_name
    response = requests.delete(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_dev_server_events(self, dev_name):
    """Get events of the dev server.

    Args:
      dev_name: The name of the dev server.

    Returns:
      The events of the dev server.
    """
    url = self._dev_server_url + "/" + dev_name + "/events"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def create_tensorboard_service(self, tensorboard_service):
    """Create the tensorboard_service.

    Args:
      tensorboard_service: The tensorboard_service object to create.

    Returns:
      The dictionary of tensorboard_service.
    """
    tensorboard_service_data = tensorboard_service.get_json_data()
    response = requests.post(self._tensorboard_url,
                             auth=self._auth,
                             data=tensorboard_service_data)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def list_tensorboard_services(self, org_id=None):
    """List tensorboard_services.

    Returns:
      The list of dictionary of tensorboard_services.
    """
    if org_id:
      url = self._tensorboard_url + "?org_id=" + org_id
    else:
      url = self._tensorboard_url
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))["data"]
    else:
      return response.content

  def describe_tensorboard_service(self, tensorboard_name, org_id=None):
    """Describe and get information of the tensorboard_service.

    Args:
      tensorboard_name: The name of the tensorboard_service.

    Returns:
      The dictionary of tensorboard_service.
    """
    if org_id:
      url = self._tensorboard_url + "/" + tensorboard_name + "?org_id=" + org_id
    else:
      url = self._tensorboard_url + "/" + tensorboard_name
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def delete_tensorboard_service(self, tensorboard_name):
    """Delete the tensorboard_service.

    Args:
      tensorboard_name: The name of the tensorboard_service.

    Returns:
      The response.
    """
    url = self._tensorboard_url + "/" + tensorboard_name
    response = requests.delete(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_tensorboard_service_events(self, tensorboard_name):
    """Get events of the tensorboard service.

    Args:
      tensorboard_name: The name of the tensorboard service.

    Returns:
      The events of the tensorboard service.
    """
    url = self._tensorboard_url + "/" + tensorboard_name + "/events"
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_quota(self, org_id=None):
    """Get quota.
    """
    if org_id:
      url = self._quota_url + "?org_id=" + org_id
    else:
      url = self._quota_url
    response = requests.get(url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))["data"]
    else:
      return response.content

  def do_predict(self, model_name, model_version, data_file, timeout=10.0):
    """Request generic gRPC server to predict

    Args:
      model_name: The name of the model.
      model_version: The version of the model.
      data_file: The json data file.
      timeout: The timeout of the gRPC request.
    """
    model_service = self.describe_model_service(model_name, model_version)
    if type(model_service) is dict:
      server = model_service["address"]
      return self.do_predict_server(server, model_name, data_file, timeout)
    else:
      return json.dumps({
          "error": True,
          "message": "Fail to get information of model service"
      })

  def do_predict_server(self, server, model_name, data_file, timeout=10.0):

    from predict_client import generic_predict_client

    if os.path.isfile(data_file):
      with open(data_file) as f:
        data = json.load(f)
    else:
      return {
          "error": True,
          "message": "The data file: {} doesn't exist".format(data_file)
      }

    return generic_predict_client.predict(server, model_name, data, timeout)

  def update_quota(self, quota):
    """Update quota by admin.

    Args:
      quota: The quota object with new value.
    """
    quota_data = quota.get_json_data()
    url = self._quota_url + "/" + quota.org_id
    response = requests.put(url, auth=self._auth, data=quota_data)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_frameworks(self):
    response = requests.get(self._framework_url)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def authentication(self):
    response = requests.get(self._authentication_url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content

  def get_org_id(self):
    response = requests.get(self._org_id_url, auth=self._auth)
    if response.ok:
      return json.loads(response.content.decode("utf-8"))
    else:
      return response.content
