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

try:
  from setuptools import setup
  setup()
except ImportError:
  from distutils.core import setup

setup(name="cloud_ml_sdk",
      version="0.2.11",
      author="Xiaomi",
      install_requires=["requests>=2.6.0", "pyOpenSSL>=16.1.0",
                        "argcomplete>=1.4.1", "cloud-ml-common>=0.2.2"],
      description="Xiaomi Cloud-ml SDK",
      packages=["cloud_ml_sdk", "cloud_ml_sdk.models",
                "cloud_ml_sdk.predict_client", "cloud_ml_sdk.command"],
      entry_points={
          "console_scripts": [
              "cloudml=cloud_ml_sdk.command.command:main",
              "cloudml_admin=cloud_ml_sdk.command.command_admin:main"
          ],
      })
