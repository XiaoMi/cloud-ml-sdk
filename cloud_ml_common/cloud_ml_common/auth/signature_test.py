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

from signature import Signer
import unittest


class SignerTest(unittest.TestCase):

  signer = Signer("ak", "sk")

  def test_header_value(self):
    header = {"Content-Type": "application/json"}
    self.assertEqual("application/json",
                     self.signer._get_header_value(header, "Content-Type"))
    self.assertEqual("", self.signer._get_header_value(header, "Content-MD5"))

  def test_sign(self):
    path = "/cloud_ml//v1/train"
    timestamp = "1474203860"
    content_md5 = "d41d8cd98f00b204e9800998ecf8427e"
    app_secret = "sk"

    self.assertEqual(
        self.signer._sign(path, timestamp, content_md5, app_secret),
        "\xd9\x18\x83\x1c`Z\t\x82{\x9d2V\x90\x11,\xa8\xe0E\xd9\xc6")

  def test_sign_to_base64(self):
    path = "/cloud_ml//v1/train"
    timestamp = "1474203860"
    content_md5 = "d41d8cd98f00b204e9800998ecf8427e"
    app_secret = "sk"

    self.assertEqual(
        self.signer._sign_to_base64(path, timestamp, content_md5, app_secret),
        "2RiDHGBaCYJ7nTJWkBEsqOBF2cY=")


if __name__ == "__main__":
  unittest.main()
