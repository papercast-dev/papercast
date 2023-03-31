# Getting Started
## Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

## Write your configuration file
Write a configuration file (a Python file) defining your pipelines.

Here's an example:
```{literalinclude} ./examples/config.py
```

### How the configuration file works
- Papercast pipelines turn documents (specified by identifiers like a filepath or DOI) into [Productions](./modules/productions.md)
- Each pipeline is a linear sequence of modules[^1] 
- Each module in the pipeline reads input data (as Production attributes) and attaches new output data attributes to the Production

### Connecting modules
- Modules operate on shared types
  - Papercast provides some [common types](./modules/types.md)
  - You can also define custom types
- Downstream modules need to know where to look to read the output of upstream modules
- Each module consumes and produces data identified by module-level names
- Each pipeline module accepts `input_names` and `output_names` arguments. These are `dict`s mapping module-level input and output names to their names in the pipeline




[^1]: (possible support for DAG structure in the future)
[^2]: Collectors are slightly different in that they start with document identifiers and produce Productions

## Use the CLI to start the server
```bash
papercast serve --hostname localhost --port 8000 --config config.py
```

```{toctree} 
:hidden:
:maxdepth: 1
```