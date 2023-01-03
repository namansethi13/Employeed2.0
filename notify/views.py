import json
from django.core import serializers

from django.shortcuts import render
from .models import NotificationModel

def notifications(request):
    notifications = NotificationModel.objects.filter(user = request.user)
    messages = serializers.serialize("json", notifications)

    new_messages = []
    for msg in json.loads(messages):
        new_messages.append({
                "id" : msg["pk"],
                "heading" : msg['fields']['heading'],
                "body" : msg['fields']['body'],
                "is_seen" : msg['fields']['is_seen'],
        })
    return render(request, 'notifications.html', {'notifications': new_messages})

