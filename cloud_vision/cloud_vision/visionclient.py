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

import copy
import rfc822
import time
import utils
import configs

import httpclient
from models import *

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

class VisionClient:
  IMAGE_DETECT_RESOURCE = "/v1/image:detect"
  def __init__(self, credential=None, endpoint=None, https_enables=False):
    """
    :param credential: object
      user's credential information
    :param endpoint: string
      the service cluster region user want to use
    :return: VisionClient object
    """
    self.__credential = credential
    self.__endpoint = endpoint
    if ":" in endpoint:
      token = endpoint.strip().split(":")
      self.__host = token[0]
      self.__port = int(token[1])
    else:
      self.__host = endpoint
      self.__port = 80
    self.__uri_prefix = "http://"
    self.__method = "POST"
    if https_enables:
      self.__uri_prefix = "https://"
    self.__uri = self.__uri_prefix + self.__endpoint + VisionClient.IMAGE_DETECT_RESOURCE 

  def __set_headers(self):
    headers = dict()
    headers[configs.CONTENT_TYPE] = "application/json; charset=UTF-8"
    headers[configs.DATE] = rfc822.formatdate(time.time())
    headers[configs.REQUEST_ID] = utils.request_id()
    headers[configs.CONTENT_MD5] = ""
    return headers

  def __check_parameter(self, image):
    if not isinstance(image,Image):
      raise TypeError("the image parameter of request Object must be Image instance!")
    if image.content is None and image.uri is None:
      raise VisionException(errMsg="the uri and the content of Image object can't all be None")

  def __result2obj(self, response):
    """
    convert a dict to DetectFaceResult, DetectLabelsResult
    :param response: dict
      a dict convert by json string
    :return: Object
      such as DetectFaceResult, DetectLabelsResult etc
    """
    result = None
    if response is None:
      return result
    if isinstance(response, dict) and "detectFacesResult" in response:
      result = DetectFacesResult()
      detect_faces_result = response["detectFacesResult"]
      if "faceDetails" in detect_faces_result:
        face_details_list = detect_faces_result["faceDetails"]
        face_details = []
        for x in face_details_list:
          box = x["boundingBox"]
          bounding_box = BoundingBox(left=box["left"], top=box["top"], width=box["width"], height=box['hight'])
          face_details.append(bounding_box)
        result.faceDetails = bounding_box
    if isinstance(response, dict) and "detectLabelsResult" in response:
      result = DetectLabelsResult()
      detect_labels_result = response["detectLabelsResult"]
      if "labels" in detect_labels_result:
        detect_labels_list = detect_labels_result["labels"]
        labels = []
        for x in detect_labels_list:
          label = Label(confidence=x["confidence"], name=x["name"])
          labels.append(label)
        result.labels = labels
    return result

  def load_image(self, path):
    bytes_source = None
    try:
      image_file = open(path, "r")
      bytes_source = image_file.read()
    except Exception, e:
      print Exception, ":", e
    finally:
      if image_file is not None:
        image_file.close()
    return bytes_source

  def detect_labels(self, *args, **kwargs):
    """
    # the interface form hasn't been decided, so here use the common form
    :param args:
      args[0]: ImageDetectRequest Object
    :param kwargs: dict
      Temporarily not used, remain
    :return:DetectLabelsResult Object
    """
    if not isinstance(args[0], DetectLabelsRequest):
      raise TypeError("The first argument must be a ImageDetectRequest Object!")
    # here temporary use deepcopy avoid image content be changed
    detect_labels_request = copy.deepcopy(args[0])
    image_detect_request = ImageDetectRequest()
    image_detect_request.set_detect_labels_request(detect_labels_request)
    if image_detect_request.detectLabelsRequest is not None \
        and image_detect_request.detectLabelsRequest.image is not None:
      image = image_detect_request.detectLabelsRequest.image
      self.__check_parameter(image)
      if image.content is not None:
        image_detect_request.detectLabelsRequest.image.content = \
          utils.base64_encode(image_detect_request.detectLabelsRequest.image.content)
    params = utils.obj2json(image_detect_request)
    headers = utils.auth_headers(self.__method, self.__uri, self.__set_headers(), self.__credential)
    http_conf = {"method": self.__method, "host": self.__host, "port": self.__port, "resource": self.IMAGE_DETECT_RESOURCE,
           "timeout": configs.DEFAULT_CLIENT_TIMEOUT}
    response = httpclient.execute_http_request(http_conf, params, headers)
    try:
      result = self.__result2obj(response)
      if result is None:
        raise VisionException(errMsg="error is occurred, the response is none!")
    except VisionException, ve:
      print ve
    return result

  def detect_faces(self, *args, **kwargs):
    """
    # the interface form hasn't been decided, so here use the common form
    :param args:
      args[0]: ImageDetectRequest Object
    :param kwargs: dict
      Temporarily not used, remain
    :return:DetectFacesResult Object
    """
    if not isinstance(args[0], DetectFacesRequest):
      raise TypeError("The first argument must be a DetectRequest Object!")
    # here temporary use deepcopy avoid image content be changed
    detect_faces_request = copy.deepcopy(args[0])
    image_detect_request = ImageDetectRequest()
    image_detect_request.set_detect_faces_request(detect_faces_request)
    # if only uri specified, the content will be None
    if image_detect_request.detectFacesRequest is not None \
        and image_detect_request.detectFacesRequest.image is not None:
      image = image_detect_request.detectFacesRequest.image
      self.__check_parameter(image)
      if image.content is not None:
        image_detect_request.detectFacesRequest.image.content = \
          utils.base64_encode(image_detect_request.detectFacesRequest.image.content)
    params = utils.obj2json(image_detect_request)
    headers = utils.auth_headers(self.__method, self.__uri, self.__set_headers(), self.__credential)
    http_conf = {"method": self.__method, "host": self.__host, "port": self.__port,
           "resource": self.IMAGE_DETECT_RESOURCE, "timeout": configs.DEFAULT_CLIENT_TIMEOUT}
    response = httpclient.execute_http_request(http_conf, params, headers)
    try:
      result = self.__result2obj(response)
      if result is None:
        raise VisionException(errMsg="error is occurred, the response is none!")
    except VisionException, ve:
      print ve
    return result
