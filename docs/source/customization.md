# Customization

Papercast is designed to be extensible. 

## Creating a Pipeline Component

The most straightforward customization is to create a new pipeline component. Pipeline Components are the building blocks of Papercast pipelines. There are three base classes that Pipeline Components can inherit from: `BaseProcessor`, `BaseSubscriber`, and `BasePublisher`.

### BaseProcessor

`BaseProcessor` is a base class for Pipeline Components that process a document or document identifier and return an updated document. `BaseProcessor` has two class attributes, `input_types` and `output_types`, which define the expected input and output of the Pipeline Component.

Subclasses of `BaseProcessor` must implement the abstract `process` method, which takes an instance of `Production` as input and returns an instance of `Production`. The `process` method should contain the logic for processing the input document and returning an updated document.

```python
@abstractmethod
def process(self, input: Production, *args, **kwargs) -> Production:
```

### BaseSubscriber

`BaseSubscriber` is a base class for Pipeline Components that initiate document processing based on external events, like a webhook. Subclasses of `BaseSubscriber` must implement the abstract `subscribe` method, which should contain the logic for subscribing to the external event and triggering document processing.

```python
@abstractmethod
async def subscribe(self) -> Production:
```

### BasePublisher

`BasePublisher` is a base class for Pipeline Components that publish documents to an external system. `BasePublisher` has one class attribute, `input_types`, which defines the expected input of the Pipeline Component.

Subclasses of `BasePublisher` must implement the abstract `process` method, which takes an instance of `Production` as input and publishes it to an external system. The `process` method should contain the logic for publishing the input document.

```python
@abstractmethod
def process(self, input: Production, *args, **kwargs) -> None:
```

## Step 1: Choose a Base Class

**Processor:** Choose this if you want to process a document or document identifier and return an updated document. 

**Subscriber:** Choose this if you want to initiate document processing based on external events, like a webhook.

**Publisher:** Choose this if you want to publish documents to an external system.


## Step 2: Create the Component

To create a new Pipeline Component, you will need to create a new Python class that inherits from one of the base classes: `BaseProcessor`, `BaseSubscriber`, or `BasePublisher`. 

For example, to create a new Processor, you can create a class that inherits from `BaseProcessor`:

```python
class MyProcessor(BaseProcessor):
    input_types = {"my_input": str}
    output_types = {"my_output": str}

    def process(self, input: Production, *args, **kwargs) -> Production:
        """
        Processes a document by returning the input string with "processed" appended.

        Args:
            input (Production): The input document containing a "my_input" attribute.

        Returns:
            Production: The processed document containing a "my_output" attribute.
        """
        input_string = getattr(input, "my_input")
        processed_string = f"{input_string} processed"
        output = Production(my_output=processed_string)
        return output
```

In this example, `MyProcessor` inherits from `BaseProcessor` and defines the expected input and output types using the `input_types` and `output_types` class attributes. It also implements the `process` method to perform the processing logic and return the processed document. 

You can customize the implementation of the `process` method to suit your specific use case. Once your new Pipeline Component is defined, you can instantiate it and use it as part of a Pipeline to perform your desired document processing.

## Step 3: Define Input and Output Types

When defining a new Pipeline Component, you will need to specify the expected input and output types of the component. This is done using the `input_types` and `output_types` class attributes, which are dictionaries that map attribute names to their expected data types.

For example, to define the input and output types for a custom Processor that takes a string as input and returns an integer as output, you can define the class like this:

```python
class MyProcessor(BaseProcessor):
    input_types = {"input_string": str}
    output_types = {"output_int": int}

    def process(self, input: Production, *args, **kwargs) -> Production:
        """
        Processes a document by converting the input string to an integer and returning it.

        Args:
            input (Production): The input document containing an "input_string" attribute.

        Returns:
            Production: The processed document containing an "output_int" attribute.
        """
        input_string = getattr(input, "input_string")
        output_int = int(input_string)
        output = Production(output_int=output_int)
        return output
```

In this example, `MyProcessor` defines the expected input and output types using the `input_types` and `output_types` class attributes. The `input_types` attribute specifies that the input document should have an attribute named "input_string" that is of type `str`. The `output_types` attribute specifies that the processed document should have an attribute named "output_int" that is of type `int`.

You can customize the input and output types of your Pipeline Component to match your specific use case.


## Step 4: Share your Pipeline Component (Optional)

If you would like to share your Pipeline Component with the Papercast community, you can follow the steps at the [contributing guide](./contributing.md).