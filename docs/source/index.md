# Papercast
An extensible framework to turn technical documents into multimedia. Written in Python.


```{raw} html

    <iframe src="_static/plugins.html" height="345px" width="100%"></iframe>
```

*More plugins coming soon! Write your own!*

## Features
- Add documents in multiple formats, from popular sources:
- Define pipelines to process documents using any tool you can think of
- Publish your productions to multiple endpoints
- Run anywhere
- Add documents from any machine with the CLI

## Pipelines
- Combine tools to create a document processing pipeline

## Interfaces
- Run your document processing pipelines standalone or give them an API with [Papercast Server](server/server.md).
- Add documents from other devices with the [Papercast CLI](cli/cli.md).


## Pipeline Components

Papercast is designed around 3 types of modules:

- [Collectors](modules/collectors.md) accept document identifiers and return [Productions](modules/productions.md).
- [Processors](modules/processors.md) modify Productions.
- [Publishers](modules/publishers.md) publish Productions to your desired endpoint (e.g. a podcast feed, Twitter (coming soon), etc).

Customize the behavior at each of these steps by writing your own modules.


```{toctree}
:caption: Modules
:hidden:
./modules/collectors.md
./modules/processors.md
./modules/publishers.md
./modules/productions.md
./modules/types.md
```

```{toctree}
:caption: Pipelines
:hidden:
./modules/pipelines.md
```

```{toctree}
:caption: API Reference
:hidden:
./api_reference.md
```