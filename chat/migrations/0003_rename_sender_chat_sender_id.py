# Generated by Django 4.1.7 on 2023-10-19 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_remove_chat_reciever_chat_sender_type_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='sender',
            new_name='sender_id',
        ),
    ]
