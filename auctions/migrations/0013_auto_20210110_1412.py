# Generated by Django 3.1.4 on 2021-01-10 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auto_20210110_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('electronics', 'Electronics'), ('fashion', 'Fashion'), ('home', 'Home'), ('other', 'Other'), ('toys', 'Toys')], default='other', max_length=20),
        ),
    ]
