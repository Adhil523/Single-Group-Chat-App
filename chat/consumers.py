import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("Reached connect")

        self.room_group_name='test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )


        self.accept()
        self.send(text_data=json.dumps({         #the message is being sent to the html page to the backend
            'type':'connection_estbaished',
            'message':'You are now connected'
        }))
    def receive(self,text_data):
        print("Reached receive")
        print(text_data)
        print(type(text_data))
        text_data_json=json.loads(text_data)
        print(text_data_json)
        print(type(text_data_json))
        message=text_data_json['message']
        print('message:',message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message
            }
        )
    def chat_message(self,event):
        message=event['message']
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))



        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message':message
        # }))