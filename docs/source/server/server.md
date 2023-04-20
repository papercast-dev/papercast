```{toctree} 
:hidden:
:maxdepth: 1
```

# Papercast Server

The Papercast Server is a Python web application that provides a framework for creating and running text processing pipelines. The server exposes an API that allows clients to add documents to pipelines and retrieve information about the available pipelines and their processors.

## Requirements

To run the Papercast Server, you'll need:

    Python 3.7 or later
    The FastAPI and uvicorn libraries
    The papercast package

## Installation

To install the Papercast Server, you can use pip:

```
pip install git+https://github.com/papercast-dev/papercast.git
```


## Usage

To create a Papercast Server instance, you'll need to provide it with a dictionary of pipelines. Each pipeline should be an instance of the [papercast.pipelines.Pipeline](../modules/pipelines.md) class.

Once you've created a Server instance, you can start the server by calling its `.run()` method:

```python
from papercast import Pipeline
from papercast.server import Server

pipeline = Pipeline(name="my_pipeline")
# Add components to the Pipeline and connect them here...

server = Server(pipelines={"my_pipeline": pipeline})
server.run()
```

This will start the server on the default host and port (localhost:8000). You can specify a different host and/or port by passing them as arguments to the run() method:

```python
server.run(host="X.X.X.X", port=XXXX)
```

## Endpoints

The Papercast Server exposes the following API endpoints:

    /add: Add a document to a pipeline.
    /pipelines: List available pipelines and their processors.

### POST /add

Add a document to a pipeline.

#### Request Body

The request body should be a JSON object containing the following fields:

    pipeline: The name of the pipeline to add the document to.
    Additional fields representing the document data to be processed.

#### Response

On success, the server will return a JSON object with a message field indicating that the document was added to the pipeline.

On failure, the server will return an HTTP error code and a JSON object with an error field containing a description of the error.

### GET /pipelines

List available pipelines and their processors.

#### Response

The server will return a JSON object with a pipelines field containing a dictionary of pipeline names and their corresponding processing steps.