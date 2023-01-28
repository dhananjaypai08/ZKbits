# Generated by Django 4.1.5 on 2023-01-28 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('category', models.CharField(max_length=200)),
                ('mode', models.CharField(max_length=200)),
                ('totalamount', models.IntegerField()),
                ('description', models.TextField()),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]