## Introduction

`generic_predict_client.py` is the python gRPC client for TensorFlow serving. It parses JSON data into TensorProto and request gRPC service for inference.

## Usage

It is easy to run with command-line arguments.

```
generic_predict_client.py --server 127.0.0.1:9000 --model cancer --data ./cancer.json
```

The example JSON file looks like this.

```
{
  "keys_dtype": "int32",
  "keys": [[1], [2]],
  "X_dtype": "float32",
  "X": [[10.0], [30.0]]
}
```
