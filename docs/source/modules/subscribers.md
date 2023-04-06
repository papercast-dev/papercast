# Subscribers

Subscribers can be used to wait for events and trigger pipeline runs when they occur.

Each subscriber implements a .subscribe() method that returns an async iterator. 
The iterator yields events as they occur. 
The subscriber is responsible for filtering out events that are not relevant to the pipeline.

