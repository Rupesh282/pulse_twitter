# Generated by Django 4.0 on 2021-12-14 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0003_posts_posttotags_delete_test0'),
    ]

    operations = [
        migrations.RenameField(
            model_name='posttotags',
            old_name='post_id',
            new_name='post',
        ),
    ]
