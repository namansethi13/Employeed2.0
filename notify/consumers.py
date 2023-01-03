import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, JsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import NotificationModel
from django.core import serializers

class NotifyConsumer(WebsocketConsumer):

    def get_unseen_notification(self):
        notifications = NotificationModel.objects.filter(user = self.scope["user"], is_seen=False)
        messages = serializers.serialize("json", notifications)

        new_messages = []
        for msg in json.loads(messages):
            new_messages.append({
                "id" : msg["pk"],
                "heading" : msg['fields']['heading'],
                "body" : msg['fields']['body'],
                "is_seen" : msg['fields']['is_seen'],
            })
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type' : 'chat_message',
                'messages' : new_messages,
            }
        )

    def update_notification(self, id):
        notification = NotificationModel.objects.get(id=int(id))
        notification.is_seen = True
        notification.save()

    def connect(self):
        self.room_group_name = self.scope["user"].username
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        
        self.get_unseen_notification()
        

    def receive(self, text_data=None, bytes_data=None):
        print("Received message")
        text_data_json = json.loads(text_data)
        print("json = ", text_data_json)
        id = text_data_json['id']

        self.update_notification(id)
        self.get_unseen_notification()

    # Receive message from room group
    def chat_message(self, event):
        messages = event['messages']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type' : 'chat',
            'messages': messages,
            'count' : len(messages)
        }))

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )