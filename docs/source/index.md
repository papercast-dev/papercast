# Papercast
An extensible framework to turn technical documents into multimedia. Written in Python.

## Features
- Add documents in multiple formats, from popular sources:
    - [ArXiV](https://github.com/papercast-dev/papercast-arxiv)
    - [SemanticScholar](https://github.com/papercast-dev/papercast-semanticscholar)
    - ... and more! Write your own!
- Define pipelines to process documents using any tool you can think of
    - [GROBID]() for PDF extraction
    - TTS tools for narration
    - ... and more! Summarization, other AI tools, etc. coming soon! Write your own!
- Publish your productions to multiple endpoints
    - Self-hosted RSS podcast using GitHub Pages
    - Any other endpoint you can think of! Seriously, write a plugin!
- Run anywhere
- Add documents from any machine with a terminal with the CLI

## Interfaces
- Run your document processing pipelines standalone or give them an API with [Papercast Server](server/server.md).
- Add documents from other devices with the [Papercast CLI](cli/cli.md).

## Pipelines
- Combine tools to create a document processing pipeline


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