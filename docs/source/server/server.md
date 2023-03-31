# Server
```{toctree} 
:hidden:
:maxdepth: 1
```

- Each papercast instance gets a server
- Papercast Server is configured with [pipelines](../modules/pipelines.md)
- Each Server can have multiple Pipelines
- Papercast Server makes several methods available:
  - `/api/status` Get the status of the papercast instance
  - `/api/add` Add a document to the papercast instance
  - `/api/pipelines` Get the pipelines available at this papercast instance