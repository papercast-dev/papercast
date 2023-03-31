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
- Add documents from other devices with **Papercast Client** and **Papercast CLI**.

## Modules
```{mermaid}
graph LR
    Collect --> Extract --> Filter --> Narrate --> Publish
```
Papercast is designed around 5 types of modules:

- [Collectors](modules/collectors.md) add documents to the project.
- [Extractors](modules/extractors.md) convert documents to a usable format.
- [Filters](modules/filters.md) transform the document (as simple as removing line breaks, or as complex as using a language model to generate a summary).
- [Narrators](modules/narrators.md) convert the text to audio.
- [Publishers](modules/publishers.md) publish the result to your desired endpoint (e.g. a podcast feed).

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
./modules/extractors.md
./modules/filters.md
./modules/narrators.md
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