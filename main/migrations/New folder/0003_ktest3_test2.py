# Generated by Django 4.2.5 on 2023-10-27 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_basemodel_modelnames_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ktest3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Ktest3',
                'db_table': 'main_ktest3',
            },
        ),
        migrations.CreateModel(
            name='Test2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Test2',
                'db_table': 'main_test2',
            },
        ),
    ]
