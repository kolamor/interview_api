# Generated by Django 2.2.10 on 2020-09-21 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskfb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='ended_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='interview',
            name='started_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
