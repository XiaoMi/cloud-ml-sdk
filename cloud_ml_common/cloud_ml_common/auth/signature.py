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

import base64
import hashlib
from hashlib import sha1
import hmac
import sys
import time
try:
  from urllib.parse import urlparse
except ImportError:
  from urlparse import urlparse
from requests.auth import AuthBase

from .constant import Constant


class Signer(AuthBase):
  """The signer class used to sign the request."""

  def __init__(self, app_key, app_secret):
    self._app_key = str(app_key)
    self._app_secret = str(app_secret)

  def __call__(self, request):
    path = urlparse(request.url).path
    if not request.body:
      request.body = ""
    timestamp = request.headers.get(Constant.TIMESTAMP, str(int(time.time())))
    if sys.version_info > (3, 0):
      content_md5 = request.headers.get(
          Constant.CONTENT_MD5,
          hashlib.md5(request.body.encode("utf-8")).hexdigest())
    else:
      content_md5 = request.headers.get(Constant.CONTENT_MD5,
                                        hashlib.md5(request.body).hexdigest())

    request.headers[Constant.TIMESTAMP] = timestamp
    request.headers[Constant.CONTENT_MD5] = content_md5
    request.headers[
        Constant.
        AUTHORIZATION] = Constant.AUTHORIZATION_PREFIX + self._sign_to_base64(
            path, timestamp, content_md5, self._app_secret)
    request.headers[Constant.SECRET_KEY_ID] = self._app_key
    return request

  def _sign(self, path, timestamp, content_md5, app_secret):
    """Sign the specified http request."""

    string_to_sign = "{}\n{}\n{}\n".format(path, timestamp, content_md5)
    if sys.version_info > (3, 0):
      digest = hmac.new(
          app_secret.encode("utf-8"),
          string_to_sign.encode("utf-8"),
          digestmod=sha1)
    else:
      digest = hmac.new(app_secret, string_to_sign, digestmod=sha1)
    return digest.digest()

  def _sign_to_base64(self, path, timestamp, content_md5, app_secret):
    """Sign the specified request to base64 encoded result."""

    signature = self._sign(path, timestamp, content_md5, app_secret)
    if sys.version_info > (3, 0):
      return base64.encodestring(signature).strip().decode("utf-8")
    else:
      return base64.encodestring(signature).strip()

  def _get_header_value(self, http_headers, name):
    if http_headers is not None and name in http_headers:
      value = http_headers[name]
      if type(value) is list:
        return http_headers[name][0]
      else:
        return value
    return ""
