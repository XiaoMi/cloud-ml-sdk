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

import paddle.v2 as paddle
import paddle.v2.dataset.uci_housing as uci_housing


def main():
  paddle.init(use_gpu=False, trainer_count=1)

  x = paddle.layer.data(name='x', type=paddle.data_type.dense_vector(13))
  y_predict = paddle.layer.fc(input=x, size=1, act=paddle.activation.Linear())
  y = paddle.layer.data(name='y', type=paddle.data_type.dense_vector(1))
  cost = paddle.layer.mse_cost(input=y_predict, label=y)
  parameters = paddle.parameters.create(cost)
  optimizer = paddle.optimizer.Momentum(momentum=0)
  trainer = paddle.trainer.SGD(cost=cost,
                               parameters=parameters,
                               update_equation=optimizer)
  feeding = {'x': 0, 'y': 1}

  def event_handler(event):
    if isinstance(event, paddle.event.EndIteration):
      if event.batch_id % 100 == 0:
        print "Pass %d, Batch %d, Cost %f" % (event.pass_id, event.batch_id,
                                              event.cost)

    if isinstance(event, paddle.event.EndPass):
      result = trainer.test(reader=paddle.batch(uci_housing.test(),
                                                batch_size=2),
                            feeding=feeding)
      print "Test %d, Cost %f" % (event.pass_id, result.cost)

  trainer.train(reader=paddle.batch(
      paddle.reader.shuffle(uci_housing.train(),
                            buf_size=500),
      batch_size=2),
                feeding=feeding,
                event_handler=event_handler,
                num_passes=30)


if __name__ == "__main__":
  main()
