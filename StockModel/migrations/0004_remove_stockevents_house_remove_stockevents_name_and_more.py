# Generated by Django 5.0.3 on 2024-03-22 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockModel', '0003_stockevents'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stockevents',
            name='house',
        ),
        migrations.RemoveField(
            model_name='stockevents',
            name='name',
        ),
        migrations.AlterField(
            model_name='stockevents',
            name='event_remark',
            field=models.CharField(blank=True, default='', max_length=1000, null=True),
        ),
    ]
