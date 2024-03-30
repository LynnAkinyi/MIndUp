from channels.generic.websocket import AsyncWebsocketConsumer
import json



class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        time = text_data_json["time"]
        recipient_channel_name = text_data_json.get("recipient_channel_name")

        if recipient_channel_name:
            # Handle direct chat messages
            await self.channel_layer.send(
                recipient_channel_name,
                {
                    "type": "send_message",
                    "message": message,
                    "username": username,
                    "time": time
                }
            )
        else:
            # Handle group chat messages
            await self.channel_layer.group_send(
                "group-chat",
                {
                    "type": "send_message",
                    "message": message,
                    "username": username,
                    "time": time
                }
            )

    async def send_message(self, event):
        message = event["message"]
        username = event["username"]
        time = event["time"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "time": time}))


