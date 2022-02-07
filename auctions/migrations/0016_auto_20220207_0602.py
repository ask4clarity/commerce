# Generated by Django 3.1.3 on 2022-02-07 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20220207_0601'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='user',
            name='watching',
        ),
        migrations.RemoveField(
            model_name='user',
            name='winner',
        ),
        migrations.AddField(
            model_name='listing',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='creator', to='auctions.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='listing',
            name='watching',
            field=models.ManyToManyField(related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='listing',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='top', to=settings.AUTH_USER_MODEL),
        ),
    ]
