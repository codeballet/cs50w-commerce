# Generated by Django 3.2.5 on 2021-07-08 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0027_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='user_id',
            new_name='user',
        ),
    ]
