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
except ImportError:
  from distutils.core import setup

setup(name="cloud_ml_common",
      version="0.2.2",
      author="Xiaomi",
      license="Apache License",
      description="Xiaomi Cloud-ml Common",
      install_requires=["requests>=2.6.0"],
      packages=["cloud_ml_common", "cloud_ml_common.auth"])
