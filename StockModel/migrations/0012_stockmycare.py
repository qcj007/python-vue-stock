# Generated by Django 5.0.3 on 2024-04-09 23:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockModel', '0011_stockzcw_lb'),
    ]

    operations = [
        migrations.CreateModel(
            name='stockMyCare',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=30)),
                ('update_time', models.DateTimeField(null=True)),
            ],
        ),
    ]
