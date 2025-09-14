
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels_redis.core import RedisChannelLayer

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.propagate = True

class ChatConsumer(AsyncWebsocketConsumer):
    # Store last message timestamps per user in memory (per process)
    user_last_message_time = {}

    async def connect(self):
        self.room_group_name = 'chat_room'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        # Send message history from Redis
        messages = await self.get_message_history_from_redis()
        for msg in messages:
            if isinstance(msg, dict):
                await self.send(text_data=json.dumps({
                    'user_id': msg.get('user_id', '-'),
                    'sender': msg.get('sender', 'Anonymous'),
                    'message': msg.get('message', '')
                }))
            else:
                await self.send(text_data=json.dumps({
                    'user_id': '-',
                    'sender': 'Anonymous',
                    'message': msg
                }))
    @database_sync_to_async
    def get_message_history_from_redis(self):
        from django.conf import settings
        import redis
        r = redis.Redis(host='redis', port=6379, db=0)
        messages = r.lrange('chat_messages', 0, -1)
        result = []
        for m in messages:
            try:
                obj = json.loads(m.decode('utf-8'))
                result.append(obj)
            except Exception:
                result.append({'user_id': '-', 'sender': 'Anonymous', 'message': m.decode('utf-8')})
        return result

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_id = self.scope["user"].id if self.scope["user"].is_authenticated else None
        sender = self.scope["session"].get("user_name", "Anonymous")
        if 'typing' in data:
            logger.info(f"User {sender} (ID: {user_id}) typing: {data['typing']}")
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_event',
                    'sender': sender,
                    'typing': data['typing']
                }
            )
            return
        message = data.get('message', '')
        import time
        now = time.time()
        # Only rate limit authenticated users
        if user_id:
            last_time = ChatConsumer.user_last_message_time.get(user_id, 0)
            if now - last_time < 5:
                logger.warning(f"Rate limit: User {sender} (ID: {user_id}) tried to send a message before 5 seconds elapsed.")
                # Send alert to user only
                await self.send(text_data=json.dumps({
                    'alert': 'You can send a message every 5 seconds.'
                }))
                return
            ChatConsumer.user_last_message_time[user_id] = now
        msg_obj = {'user_id': user_id, 'sender': sender, 'message': message}
        logger.info(f"User {sender} (ID: {user_id}) sent message: {message}")
        # Store message in Redis
        await self.save_message_to_redis(json.dumps(msg_obj))
        # Broadcast message to group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_id': user_id,
                'sender': sender,
                'message': message
            }
        )
    async def typing_event(self, event):
        await self.send(text_data=json.dumps({
            'sender': event.get('sender', 'Anonymous'),
            'typing': event.get('typing', False)
        }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event.get('user_id', '-'),
            'sender': event.get('sender', 'Anonymous'),
            'message': event.get('message', '')
        }))

    @database_sync_to_async
    def save_message_to_redis(self, message):
        from django.conf import settings
        import redis
        r = redis.Redis(host='redis', port=6379, db=0)
        r.rpush('chat_messages', message)
