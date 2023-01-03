import json
from channels.generic.websocket import WebsocketConsumer
from django.core import serializers
from celery import shared_task
from asgiref.sync import async_to_sync
from celery.utils.log import get_task_logger
import requests
from core.settings import DOMAIN

logger = get_task_logger(__name__)


class TestSubmission(WebsocketConsumer):

    def connect(self):
        self.room_group_name = self.scope["user"].username
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.send(text_data=json.dumps({
            'type' : 'markQuestion',
            'messages': 'questionList',
            'questionList' : [None, None, 'A', 'D', 'B', 'D']
        }))

    
    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
    
    # Receiving message from outside consumber
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json['type'] == "question_list":
            message = text_data_json['questionList']
        # Print message that receive from Websocket
        
            print(message)

      
    def submitTest(self, event):
        messages = event['messages']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type' : 'chat',
            'messages': messages
        }))


@shared_task
def request_for_submit_test(*args, **kwargs):
    response = requests.post(f'{DOMAIN}/submit/', data={'group_name': kwargs['username']})
    if response.status_code == 200:
        logger.info("Status is 200")
    else:
        logger.info(f"Status is {response.status_code}")
