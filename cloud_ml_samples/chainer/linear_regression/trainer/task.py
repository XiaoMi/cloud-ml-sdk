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

import numpy as np

from chainer import FunctionSet, Variable, optimizers, serializers
import chainer.links as L
import chainer.functions as F
import chainer


def main():
  # Define train function
  def linear_train(train_data, train_target, n_epochs=200):
    for _ in range(n_epochs):
      output = linear_function(train_data)
      loss = F.mean_squared_error(train_target, output)
      linear_function.zerograds()
      loss.backward()
      optimizer.update()

  # Construct train data
  x = 30 * np.random.rand(1000).astype(np.float32)
  y = 7 * x + 10
  y += 10 * np.random.randn(1000).astype(np.float32)

  linear_function = L.Linear(1, 1)

  x_var = Variable(x.reshape(1000, -1))
  y_var = Variable(y.reshape(1000, -1))

  optimizer = optimizers.MomentumSGD(lr=0.001)
  optimizer.setup(linear_function)

  for i in range(150):
    linear_train(x_var, y_var, n_epochs=20)
    y_pred = linear_function(x_var).data

  slope = linear_function.W.data[0, 0]
  intercept = linear_function.b.data[0]

  print("Final Line: {0:.3}x + {1:.3}".format(slope, intercept))


if __name__ == "__main__":
  main()
