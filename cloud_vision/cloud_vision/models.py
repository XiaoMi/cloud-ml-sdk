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

import urlparse
import visionconfig

class Credential:
  def __init__(self, galaxy_access_key=None, galaxy_key_secret=None):
    """
    :param galaxy_access_key: string
    user's access key id
    :param galaxy_key_secret: string
    user's secret access key
    :return : Credential object
    """
    self.galaxy_access_key = galaxy_access_key
    self.galaxy_key_secret = galaxy_key_secret

class Image:
  def __init__(self, uri=None, content=None):
    if uri is not None:
      self.__check_uri(uri)
    self.uri = uri
    if content is not None:
      self.__check_content(content)
    self.content = content

  def __check_uri(self, uri):
    url = urlparse.urlparse(uri)
    if url.scheme != visionconfig.FDS_URI_SCHEME:
      raise Exception("uri scheme %s is not support, only support fds scheme now" % url.scheme)
    if not uri.endswith(".jpg"):
      raise Exception("this image format is not support, only support jpg and png format now")

  def __check_content(self, content):
    if isinstance(content, str):
      if len(content) > visionconfig.MAX_REQUEST_IMAGE_SIZE:
        raise Exception("image length exceeded, max allowed: %d" % visionconfig.MAX_REQUEST_IMAGE_SIZE)
    else:
      raise Exception("content should be a str type variable")

  def set_uri(self, uri):
    self.__check_uri(uri)
    self.uri = uri

  def set_content(self, content):
    self.__check_content(content)
    self.content = content


class DetectFacesRequest:
  def __init__(self, image=None):
    self.image = image

  def set_image(self, image):
    self.image = image


class DetectLabelsRequest:
  def __init__(self, image=None):
    self.image = image

  def set_image(self, image):
    self.image = image


class ImageDetectRequest:
  def __init__(self):
    self.detectFacesRequest = None
    self.detectLabelsRequest = None

  def set_detect_faces_request(self, detect_faces_request):
    self.detectFacesRequest = detect_faces_request

  def set_detect_labels_request(self, detect_labels_request):
    self.detectLabelsRequest = detect_labels_request


class BoundingBox:
  def __init__(self, left=None, top=None, width=None, height=None):
    self.left = left
    self.top = top
    self.width = width
    self.height = height


class FaceDetail:
  def __init__(self, bounding_box=None):
    self.boundingBox = bounding_box


class DetectFacesResult:
  def __init__(self, face_details=None):
    self.faceDetails = face_details


class Label:
  def __init__(self, confidence=None, name=None):
    self.confidence = confidence
    self.name = name


class DetectLabelsResult:
  def __init__(self, labels=None):
    self.labels = labels


class VisionException(Exception):
  def __init__(self, errorCode=None, errMsg=None, details=None, requestID=None):
    self.errorCode = errorCode
    self.errMsg = errMsg
    self.details = details
    self.requestId = requestID

  def __str__(self):
    return repr(self)

  def __repr__(self):
    L = ['%s=%r' % (key, value) for key, value in self.__dict__.iteritems()]
    return '%s(%s)' % (self.__class__.__name__, ', '.join(L))
