from papercast.base import BaseSubscriber
from abc import ABC, abstractmethod
from papercast.production import Production
from typing import AsyncIterable
from websockets.client import connect
import json

class WebSocketSubscriber(BaseSubscriber):
    def __init__(self, url) -> None:
        super().__init__()
        self.url = url

    def process(self, input: Production, *args, **kwargs) -> Production: # TODO: might not need this
        return input
    
    # @abstractmethod
    def process_message(self, message) -> Production:
        # process the message and return a Production object
        message = json.loads(message)
        print(message)
        return self.process(Production(**message))
    
    async def subscribe(self) -> AsyncIterable[Production]:
        async with connect(self.url) as socket:
            print("connected")
            async for message in socket:
                yield self.process_message(message)
