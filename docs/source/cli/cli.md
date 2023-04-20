```{toctree} 
:hidden:
:maxdepth: 1
```
# Papercast CLI

The Papercast CLI is a command-line interface for interacting with a Papercast server.

## Requirements

To use the Papercast CLI, you'll need:

- Python 3.7 or later
- The requests library
- A running Papercast [server](../server/server.md)

## Installation

The papercast CLI gets installed automatically with Papercast.

```
pip install git+https://github.com/papercast-dev/papercast.git
```

## Usage

The Papercast CLI provides a simple command-line interface for calling endpoints on a Papercast server. The available endpoints and parameters depend on the specific implementation of the Papercast server, but common endpoints include:

- `/add`: Add a document to a pipeline.
- `/pipelines`: List available pipelines and their processors.

To call an endpoint, use the `papercast` command with the following syntax:

```
papercast <endpoint> [--<key> <value> ...] [--hostname <hostname>] [--port <port>]
```

Replace `<endpoint>` with the name of the endpoint to call. Additional parameters can be specified using the `--<key> <value>` syntax. For example:

```
papercast add --pipeline my_pipeline --arxiv_id 1706.03762
```

The `--hostname` and `--port` options can be used to specify the hostname or IP address and port number of the Papercast server. By default, the hostname is `"localhost"` (your local machine) and the port is `8000`.

## Troubleshooting

If you're having trouble using the Papercast CLI, make sure that:

- The Papercast server is running and accessible from your machine.
- The correct hostname and port number are specified (if necessary) using the `--hostname` and `--port` options.