# Generated by Django 5.0.6 on 2024-07-04 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('haloinfinite', '0003_servicerecord'),
    ]

    operations = [
        migrations.AddField(
            model_name='xboxuser',
            name='refresh_token',
            field=models.CharField(null=True),
        ),
    ]
