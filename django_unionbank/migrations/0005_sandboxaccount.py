# Generated by Django 3.0.7 on 2020-07-31 09:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_unionbank', '0004_pesonetbank'),
    ]

    operations = [
        migrations.CreateModel(
            name='SandBoxAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('user_id', models.CharField(max_length=32)),
                ('account_number', models.CharField(max_length=32)),
                ('card_number', models.CharField(max_length=32)),
                ('account_name', models.CharField(max_length=32)),
                ('account_code', models.CharField(max_length=32)),
                ('account_type', models.CharField(max_length=32)),
                ('status', models.CharField(max_length=32)),
                ('branch', models.CharField(max_length=32)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]
