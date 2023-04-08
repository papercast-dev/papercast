from websockets.client import connect
from typing import AsyncIterable
import json
from papercast.base import BaseSubscriber
from papercast.production import Production

from pyzotero import zotero

class ZoteroSubscriber(BaseSubscriber):
    def __init__(self, api_key: str, user_id: str) -> None:
        super().__init__()
        self.url = "ws://stream.zotero.org"
        self.api_key = api_key
        self.user_id = user_id
        self.zot = zotero.Zotero(user_id, "user", api_key)
        self.subscription_message = {
            "action": "createSubscriptions",
            "subscriptions": [
                {
                    "apiKey": api_key,
                    "topics": [
                        f"/users/{user_id}",
                    ]
                },
            ]
        }

    async def _subscribe_topic(self, socket):
        await socket.send(json.dumps(self.subscription_message))            
        response = await socket.recv()
        response_data = json.loads(response)

        if response_data["event"] == "subscriptionsCreated":
            errors = response_data.get("errors", [])
            
            if errors:
                raise ValueError(f"Error(s) creating subscriptions: {errors}")
        else:
            raise ValueError(f"Unexpected response: {response_data}")
        
        print("Subscriptions created successfully.")
    
    def process_message(self, message) -> Production:
        message = json.loads(message)
        if message["event"] == "topicUpdated":
            items = self.zot.top(limit=1)
            for item in items:
                print(item["data"]) # type: ignore
            return Production(**message)
        else:
            raise ValueError(f"Unexpected message: {message}")

    async def subscribe(self) -> AsyncIterable[Production]:
        print("\n\n")
        print(self.url)

        print("\n\n")
        async with connect(self.url) as socket:
            await self._subscribe_topic(socket)
            async for message in socket:
                yield self.process_message(message)