# Generated by Django 4.2.16 on 2024-11-08 06:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_candidate_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalscoutmail',
            name='scout_sender_reason',
            field=models.TextField(blank=True, default='', verbose_name='差出人の選択理由'),
        ),
        migrations.AddField(
            model_name='scoutmail',
            name='scout_sender_reason',
            field=models.TextField(blank=True, default='', verbose_name='差出人の選択理由'),
        ),
    ]
