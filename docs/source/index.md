# Papercast
An extensible framework to turn technical documents into multimedia. Written in Python.

## Features
- Add documents in multiple formats, from popular sources
- Define text extraction and narration pipelines
- Publish your productions to multiple endpoints
- Run anywhere
- Add documents from anywhere

## Interfaces
- Run your document processing pipelines with **Papercast Server**.
- Add documents from other devices with the **Papercast CLI**.

## Modules
```{mermaid}
graph LR
    Collect --> Process --> Publish
```
Papercast is designed around 5 types of modules:

- [Collectors](modules/collectors.md) accept document identifiers and return Productions.
- [Processors](modules/extractors.md) modify Productions.
- [Publishers](modules/publishers.md) publish Productions to your desired endpoint (e.g. a podcast feed, Twitter, etc).

Customize the behavior at each of these steps by writing your own modules.

```{toctree}
:caption: Getting Started
:hidden:
getting_started.md
```

```{toctree}
:caption: Modules
:hidden:
./modules/collectors.md
./modules/processors.md
./modules/publishers.md
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