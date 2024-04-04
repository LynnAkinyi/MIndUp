# your_project/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from myapp.consumer import ChatConsumer
from myapp import consumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<uniqueId>[0-9]+)/$', consumer.ChatConsumer.as_asgi()),
]


application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
