from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from courses.models import BlockStudent, Course, Enrolment


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.course_id = self.scope['url_route']['kwargs']['course_id']

        allowed = await self.user_can_access_chat()

        if not allowed:
            await self.close()
            return

        self.room_group_name = f'course_chat_{self.course_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive_json(self, content):
        message = content.get('message', '').strip()

        if not message:
            return

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.scope['user'].username,
            }
        )

    async def chat_message(self, event):
        await self.send_json(
            {
                'message': event['message'],
                'username': event['username'],
            }
        )

    @database_sync_to_async
    def user_can_access_chat(self):
        user = self.scope['user']

        if not user.is_authenticated:
            return False

        course = Course.objects.filter(id=self.course_id).first()

        if course is None:
            return False

        if course.teacher == user:
            return True

        if user.role != 'STUDENT':
            return False

        blocked = BlockStudent.objects.filter(
            teacher=course.teacher,
            student=user,
            course=course
        ).exists()

        if blocked:
            return False

        return Enrolment.objects.filter(
            course=course,
            student=user
        ).exists()