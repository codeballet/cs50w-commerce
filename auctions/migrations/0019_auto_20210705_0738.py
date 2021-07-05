# Generated by Django 3.2.5 on 2021-07-05 07:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_user_bids'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='listing',
            new_name='listing_id',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bids',
        ),
        migrations.AddField(
            model_name='bid',
            name='user_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
