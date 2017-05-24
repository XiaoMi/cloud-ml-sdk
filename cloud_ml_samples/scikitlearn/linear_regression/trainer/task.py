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
from sklearn import datasets, linear_model


def main():
  diabetes = datasets.load_diabetes()
  diabetes_X = diabetes.data[:, np.newaxis, 2]

  diabetes_X_train = diabetes_X[:-20]
  diabetes_X_test = diabetes_X[-20:]

  diabetes_y_train = diabetes.target[:-20]
  diabetes_y_test = diabetes.target[-20:]

  regr = linear_model.LinearRegression()
  regr.fit(diabetes_X_train, diabetes_y_train)

  print('Coefficients: \n', regr.coef_)
  print("Mean squared error: %.2f" %
        np.mean((regr.predict(diabetes_X_test) - diabetes_y_test)**2))
  print('Variance score: %.2f' % regr.score(diabetes_X_test, diabetes_y_test))


if __name__ == "__main__":
  main()
