# from channels.generic.websocket import AsyncWebsocketConsumer
# import json

# class LocationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         await self.channel_layer.group_add(
#             'guides',
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             'guides',
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         guide_id = data['guide_id']
#         latitude = data['latitude']
#         longitude = data['longitude']
#         print("==============================================================================================")
        
#         # Save the updated location in the database
#         # ...
#         # Broadcast the updated location to all connected tourist clients
#         await self.channel_layer.group_send(
#             'tourists',
#             {
#                 'type': 'location.update',
#                 'guide_id': guide_id,
#                 'latitude': latitude,
#                 'longitude': longitude

                
#             }
            
#         )
#         print(f"Sent location update for guide {guide_id}: ({latitude}, {longitude}, to tourists group")
        

#     async def location_update(self, event):
#           guide_id = event['guide_id']
#           latitude = event['latitude']
#           longitude = event['longitude']
#           await self.send(text_data=json.dumps(event))


from channels.generic.websocket import AsyncWebsocketConsumer
import json


class GuideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'guides',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'guides',
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data['latitude']
        longitude = data['longitude']
        guide_id = data['guide_id']
        guide_uname = data['guide_uname']
        print("======================================================================================================")
        print(latitude)
        # Save the updated location in the database for the guide
        # ...
        
        # Broadcast the updated location to all connected tourist clients
        await self.channel_layer.group_send(
            'tourists',
            {
                'type': 'location.update',
                'latitude': latitude,
                'longitude': longitude,
                'guide_id' : guide_id,
                'guide_uname' : guide_uname

            }
        )


class TouristConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add(
            'tourists',
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            'tourists',
            self.channel_name
        )

    async def location_update(self, event):
        latitude = event['latitude']
        longitude = event['longitude']
        guide_id =  event['guide_id']
        guide_uname = event['guide_uname']
        await self.send(text_data=json.dumps({'latitude': latitude, 'longitude': longitude,'guide_id': guide_id, 'guide_uname': guide_uname}))
