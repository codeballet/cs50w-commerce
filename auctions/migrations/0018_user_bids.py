# Generated by Django 3.2.5 on 2021-07-05 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_user_listings'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bids',
            field=models.ManyToManyField(related_name='users', to='auctions.Bid'),
        ),
    ]
