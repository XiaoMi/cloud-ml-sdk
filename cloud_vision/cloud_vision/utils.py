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

import base64
import hmac
import json
import random
import uuid
from urlparse import urlparse
from hashlib import sha1
from configs import XIAOMI_HEADER_PREFIX, CONTENT_MD5, CONTENT_TYPE, DATE, AUTHORIZATION


def obj2json(obj):
  return json.dumps(obj, skipkeys=True, default=lambda o: o.__dict__)


def request_id():
  uid = uuid.uuid1().__str__()
  return uid[:8] + "_" + str(random.randint(-1000000000000, 1000000000000))


def base64_encode(data):
  if data is not None:
    return base64.b64encode(data)
  else:
    raise TypeError("The argument of base64encode can't be None!")


def __canonicalize_xiaomi_headers(http_headers):
  if http_headers is None or len(http_headers) == 0:
    return ''
  canonicalized_headers = dict()
  for key in http_headers:
    lower_key = key.lower()
    try:
      lower_key = lower_key.decode('utf-8')
    except:
      pass
    if http_headers[key] and lower_key.startswith(XIAOMI_HEADER_PREFIX):
      if type(http_headers[key]) != str:
        canonicalized_headers[lower_key] = str()
        i = 0
        for k in http_headers[key]:
          canonicalized_headers[lower_key] += '%s' % (k.strip())
          i += 1
          if i < len(http_headers[key]):
            canonicalized_headers[lower_key] += ','
      else:
        canonicalized_headers[lower_key] = http_headers[key].strip()
  result = ""
  for key in sorted(canonicalized_headers.keys()):
    values = canonicalized_headers[key]
    result += '%s:%s\n' % (key, values)
  return result

def __canonicalize_resource(uri):
  result = ""
  parsed_url = urlparse(uri)
  result += '%s' % parsed_url.path
  query_args = parsed_url.query.split('&')
  subresource = []

  i = 0
  for query in sorted(query_args):
    key = query.split('=')
    if key[0] in subresource:
      if i == 0:
        result += '?'
      else:
        result += '&'
      if len(key) == 1:
        result += '%s' % key[0]
      else:
        result += '%s=%s' % (key[0], key[1])
      i += 1
  return result

def auth_headers(method, uri, headers, credential):
  string_to_assign = str()
  string_to_assign += '%s\n' % method
  string_to_assign += '%s\n' % headers[CONTENT_MD5]
  string_to_assign += '%s\n' % headers[CONTENT_TYPE]
  string_to_assign += '%s\n' % headers[DATE]
  string_to_assign += '%s' % __canonicalize_xiaomi_headers(headers)
  string_to_assign += '%s' % __canonicalize_resource(uri)
  signature = base64.encodestring(hmac.new(credential.galaxy_key_secret, string_to_assign, digestmod=sha1).digest()).strip()
  auth_string = "Galaxy-V2 %s:%s" % (credential.galaxy_access_key, signature)
  new_header = dict.copy(headers)
  new_header[AUTHORIZATION] = auth_string
  return new_header
