from django.db import models
from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

class NotificationModel(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE)
    heading = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.heading


# @receiver(post_save, sender=NotificationModel)
# def send_notification(sender,instance,created,**kwargs):
#     if created:
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             group = instance.user.username,
#             message= {
#                 'type' : 'chat_message',
#                 'message' : instance.heading
#             }
#         )