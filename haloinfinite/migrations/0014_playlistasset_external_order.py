# Generated by Django 5.0.6 on 2024-07-10 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haloinfinite', '0013_userplaylistcsr'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlistasset',
            name='external_order',
            field=models.IntegerField(default=0),
        ),
    ]
