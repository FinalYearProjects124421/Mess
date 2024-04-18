from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('shownewusers/',consumers.ShowNewUsers.as_asgi()),
    path('showItems/',consumers.ShowItems.as_asgi()),
    path('app/', consumers.MyConsumer.as_asgi()),
    # path('app/', consumers.MyConsumer.as_asgi()),
	# path('test/', coWebsocketConsumernsumers.TestConsumer.as_asgi()),
	# path('', consumers.ChatConsumer.as_asgi()),
    # path('admin/', consumers.WaiterConsumer.as_asgi())
    
    # # path('ws/sc/', consumers.Rao.as_asgi()),
]