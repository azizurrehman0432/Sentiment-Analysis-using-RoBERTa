# Generated by Django 4.0.3 on 2022-03-18 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newAPI', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CrawlTime',
        ),
        migrations.AddField(
            model_name='sentiment',
            name='likes_count',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
