from django.test import TestCase
from django.utils import timezone
from .models import Chat, MyAuthor
from django.urls import reverse

# class ChatModelTest(TestCase):
#     def setUp(self):
#         self.author = MyAuthor.objects.create(name='Test Author', email='test@example.com')

#     def test_create_chat(self):
#         chat = Chat.objects.create(
#             sender_id=self.author,
#             message='Test message',
#             date_created=timezone.now(),
#             room_name='Test Room',
#             sender_type=Chat.SenderType.Client
#         )
#         self.assertIsInstance(chat, Chat)
#         self.assertEqual(chat.sender_id, self.author)
#         self.assertEqual(chat.message, 'Test message')
#         self.assertEqual(chat.room_name, 'Test Room')
#         self.assertEqual(chat.sender_type, Chat.SenderType.Client)

#     def test_default_sender_type(self):
#         chat = Chat.objects.create(
#             sender_id=self.author,
#             message='Test message',
#             date_created=timezone.now(),
#             room_name='Test Room',
#         )
#         self.assertEqual(chat.sender_type, Chat.SenderType.server)

#     def test_invalid_sender_type(self):
#         with self.assertRaises(Exception):
#             Chat.objects.create(
#                 sender_id=self.author,
#                 message='Test message',
#                 date_created=timezone.now(),
#                 room_name='Test Room',
#                 sender_type='INVALID_TYPE'
#             )

#     def test_related_name_send_chats(self):
#         chat = Chat.objects.create(
#             sender_id=self.author,
#             message='Test message',
#             date_created=timezone.now(),
#             room_name='Test Room',
#             sender_type=Chat.SenderType.Client
#         )
#         self.assertEqual(self.author.send_chats.first(), chat)

#     def test_date_created_auto_now_add(self):
#         chat = Chat.objects.create(
#             sender_id=self.author,
#             message='Test message',
#             room_name='Test Room',
#             sender_type=Chat.SenderType.Client
#         )
#         self.assertIsNotNone(chat.date_created)
#         self.assertTrue(timezone.now() - chat.date_created < timezone.timedelta(seconds=1))

#     def test_room_name_max_length(self):
#         with self.assertRaises(Exception) as context:
#             Chat.objects.create(
#                 sender_id=self.author,
#                 message='Test message',
#                 date_created=timezone.now(),
#                 room_name='A' * 251, 
#                 sender_type=Chat.SenderType.Client
#             )
#         self.assertIn("value too long for type character varying(250)", str(context.exception))


# class ChatAppUrlsTest(TestCase):
#     def test_room_url(self):
#         url = reverse('room', args=[1, 2])
#         self.assertEqual(url, '/chat/room/1/2/')

#     def test_user_contacts_url(self):
#         url = reverse('user-contacts', args=[1]) 
#         self.assertEqual(url, '/chat/1/')

#     def test_delete_all_chats_url(self):
#         url = reverse('del_chats')
#         self.assertEqual(url, '/chat/delete/')