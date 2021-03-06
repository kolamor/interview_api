# Generated by Django 2.2.10 on 2020-09-23 23:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('taskfb', '0002_auto_20200921_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='text',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='taskfb.Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='interview',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='taskfb.Interview'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='answer',
            field=models.ManyToManyField(related_name='user_answers', to='taskfb.Answer'),
        ),
    ]
