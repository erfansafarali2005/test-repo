# Generated by Django 5.2 on 2025-05-02 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todo',
            old_name='date',
            new_name='created_date',
        ),
        migrations.AddField(
            model_name='todo',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
