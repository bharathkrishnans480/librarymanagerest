# Generated by Django 4.1.1 on 2022-09-23 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookshelf', '0006_rename_buy_buynow'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='pages',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]