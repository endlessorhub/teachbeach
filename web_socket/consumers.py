import json
from time import time
from datetime import datetime
import base64

from django.core.files.base import ContentFile

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from main.models import Discussion, Comment
from main.serializers import UserSerializer

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        """
        CONNECT TO WEBSOCKET
        """
        self.discussion_id = self.scope["url_route"]["kwargs"]["discussion_id"]
        self.discussion = str(self.discussion_id)
        self.user = self.scope["user"]
        print(self.user)
        print('CONNECTED')

        await self.channel_layer.group_add(self.discussion, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        """
        DISCONNECT FROM WEBSOCKET
        """
        await self.channel_layer.group_discard(
            self.discussion, 
            self.channel_name
        )


    async def receive(self, text_data):
        """
        Receive Messages From Websocket
        """
        print('RECEIVE')
        text_data_json = json.loads(text_data)

        type = text_data_json.pop('type')

        if type == 'COMMENT':
            comment_data = await self.create_comment_obj(text_data_json)
        if type == 'REPLY':
            comment_data = await self.create_comment_reply_obj(text_data_json)
        if type == 'IMAGE':
            comment_data = await self.create_comment_image_obj(text_data_json)

        await self.channel_layer.group_send(
            self.discussion, {
                "type": "send_comment", 
                "data": comment_data
            }
        )


    async def send_comment(self, event):
        """
        Send Comment Message To Websocket
        """
        print('SENDING CHAT MESSAGE')
        data = event["data"]

        await self.send(text_data=json.dumps(data))


    ### DB OPERATIONS

    @database_sync_to_async
    def create_comment_obj(self, data):
        print('CREATE COMMENT')
        c = Comment.objects.create(
            user=self.user,
            discussion=Discussion.objects.get(id=self.discussion_id),
            content=data['content'],
        )
        return {
            "type": "COMMENT",
            "id": c.id,
            "user": UserSerializer(c.user).data,
            "content": c.content,
            "created_at": str(c.created_at)
        }


    @database_sync_to_async
    def create_comment_reply_obj(self, data):
        print('CREATE REPLY COMMENT')
        c = Comment.objects.create(
            user=self.scope['user'],
            discussion=Discussion.objects.get(id=self.discussion_id),
            content=data['content'],
            reply=Comment.objects.get(id=data['parent_comment']),
            is_reply=True
        )
        return {
            "type": "REPLY",
            "id": c.id,
            "user": UserSerializer(c.user).data,
            "content": c.content,
            "parent_comment_id": c.reply.id,
            "created_at": str(c.created_at),
        }

    @database_sync_to_async
    def create_comment_image_obj(self, data):
        print('ATTACHING IMAGE')
        c = Comment.objects.get(id=data['comment_id'])

        format, imgstr = data['image_data'].split(';base64,')
        file_name = datetime.now().strftime('%Y%m-%d%H-%M%S') + "." + format.split('/')[-1]
        image = ContentFile(base64.b64decode(imgstr))

        c.image.save(file_name, image, save=True)
        return {
            "comment_id": c.id,
            "image_url": c.image.url
        }