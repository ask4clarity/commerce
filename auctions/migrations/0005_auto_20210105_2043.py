# Generated by Django 3.1.3 on 2021-01-05 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_listing_closed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='comments',
        ),
    ]