# Generated by Django 5.1.4 on 2024-12-29 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_app', '0004_alter_event_category_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
