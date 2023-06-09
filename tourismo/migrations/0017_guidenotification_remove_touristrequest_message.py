# Generated by Django 4.2 on 2023-05-08 04:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tourismo', '0016_touristrequest_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuideNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide', models.IntegerField(null=True)),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_at', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='touristrequest',
            name='message',
        ),
    ]
