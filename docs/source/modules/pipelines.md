# Pipelines
```{toctree} 
:hidden:
:maxdepth: 1
```

Papercast pipelines are a way to chain together a series of subscribers, processors, and publishers.

Subscribers respond to events and return Productions.

Processors accept Productions and return Productions.

Publishers accept Productions and return nothing in the Python environment, but may publish the Production to a remote location.  

Pipelines are constructed by connecting Processors, Processors, and Publishers together.  The output of one component is the input of the next component.  

To make pipeline components interoperable, they operate on a set of types.  Papercast provides a set of common types. More exotic use cases may require custom types.

Each processor defines a process method. Types for the input and output of the process method are defined by the input and output types of the processor.

In a sequence of processors, if the output of one processor has the same name as the output of the previous processor, this property will be updated on the Production and the previous information will be overwritten.

```python
from papercast.types import Text, Author, Title, MP3

def process(input: Production[Text, Author, Title]) -> Production[MP3]:
    ...
```
Each pipeline element has `inputs` and `outputs` that map attribute names at the global (pipeline) scope to attribute names at the processor level.