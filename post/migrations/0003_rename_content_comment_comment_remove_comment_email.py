# Generated by Django 4.0.6 on 2022-07-11 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='comment',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='email',
        ),
    ]