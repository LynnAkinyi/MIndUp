import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json.get('command')

        if command:
            if command == 'join':
                self.groupId = text_data_json['groupId']
                self.roomGroupName = f"group_chat_{self.groupId}"
                await self.channel_layer.group_add(
                    self.roomGroupName,
                    self.channel_name
                )
            elif command == 'send':
                message = text_data_json["message"]
                username = text_data_json["username"]
                time = text_data_json["time"]
                groupId = text_data_json["groupId"]
                await self.channel_layer.group_send(
                    self.roomGroupName, {
                        "type": "sendMessage",
                        "message": message,
                        "username": username,
                        "time": time,
                        "groupId": groupId
                    })

    async def sendMessage(self, event):
        message = event["message"]
        username = event["username"]
        time = event["time"]
        groupId = event["groupId"]
        await self.send(text_data=json.dumps({"message": message, "username": username, "time": time, "groupId": groupId}))
