# Generated by Django 4.2 on 2023-05-01 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourismo', '0004_guiderequest_plan_guiderequest_plan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plan',
            name='dlatitude',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='dlongitude',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='platitude',
        ),
        migrations.RemoveField(
            model_name='plan',
            name='plongitude',
        ),
        migrations.AddField(
            model_name='plan',
            name='dcoordinate',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='plan',
            name='pcoordinate',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
