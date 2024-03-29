from channels.generic.websocket import AsyncWebsocketConsumer
import json


class EmailConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'email_updates'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def email_message(self, event):
        messages = event['messages']
        await self.send(text_data=json.dumps({
            'messages': messages
        }))

    async def send_progress_to_frontend(self, event):
        progress = event['progress']
        await self.send(text_data=json.dumps({
            'progress': progress
        }))
