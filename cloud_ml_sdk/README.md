# Xiaomi Cloud-ml SDK

## Introduction

It is the Python SDK and command-line tool for Xiaomi cloud-ml service.

## Installation

Install with `pip`.

```
pip install cloud-ml-sdk
```

Install from source.

```
python ./setup install
```

## Configure

Run `cloudml init` to configure access key and secret key.

Or modify the configuration file in `~/.config/xiaomi/config`.

```
{
  "xiaomi_cloudml_endpoint": "https://cnbj3-cloud-ml.api.xiaomi.net",
  "xiaomi_access_key_id": "AKPFUxxxxxxIPKVG",
  "xiaomi_secret_access_key": "JDv8ExxxxxxxxxxxxxxrLsuB"
}
```

Or export the access key and secret as environment variables.

```
export XIAOMI_CLOUDML_ENDPOINT="https://cnbj3-cloud-ml.api.xiaomi.net"
export XIAOMI_ACCESS_KEY_ID="AKPFUxxxxxxIPKVG"
export XIAOMI_SECRET_ACCESS_KEY="JDv8ExxxxxxxxxxxxxxrLsuB"
```

## Python SDK

You can use the SDK to access Xiaomi cloud-ml service.

```
from cloud_ml_sdk.client import CloudMlClient
from cloud_ml_sdk.models.train_job import TrainJob

client = CloudMlClient("access_key", "secret_key")

train_job = TrainJob(
    "linear",
    "trainer.task",
    "fds://cloud-ml/trainer-1.0.tar.gz")

client.submit_train_job(train_job)
```

## Command-line

You can use the command-line tool to access Xiaomi cloud-ml service.

```
cloudml jobs submit -n $name -m $module -u $url

cloudml jobs list

cloudml jobs describe $name

cloudml jobs events $name

cloudml jobs logs $name

cloudml jobs delete $name
```
