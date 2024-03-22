from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from django.core.asgi import get_asgi_application
from myapp import routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # Add this line
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    ),
})
