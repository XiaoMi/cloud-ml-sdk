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
# ==============================================================================

# -*- coding: utf-8 -*-

import httplib
import json


def execute_http_request(conf, params, headers):
  """
  :param conf: dict
    http connection configuration, for example:
    {
      "uri":"xxx",
      "method":"POST",
      "timeout":xxx,
    }
  :param params: dict
    http entity

  :param headers: dict
    http header settings

  :return: dict
    response json to dict
  """
  http_client = None
  response = None
  try:
    http_client = httplib.HTTPConnection(conf["host"], port=conf["port"], timeout=conf["timeout"])
    http_client.request(conf["method"], conf["resource"], params, headers)
    response = http_client.getresponse()
    msg = response.read()
    if response.status != 200:
      raise Exception("http response status code is error, the status code is %d, the response msg is %s" % (response.status, msg))
    response = json.loads(msg, encoding='utf-8')
  except Exception, e:
    print "exception: ", e
  finally:
    if http_client:
      http_client.close()
  return response
