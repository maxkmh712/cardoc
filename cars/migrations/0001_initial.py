# Generated by Django 3.2.9 on 2021-11-28 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brandName', models.CharField(max_length=50)),
                ('brandNameEng', models.CharField(blank=True, default='', max_length=50)),
                ('country', models.CharField(blank=True, default='', max_length=50)),
            ],
            options={
                'db_table': 'brands',
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modelName', models.CharField(max_length=50)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.brand')),
            ],
            options={
                'db_table': 'models',
            },
        ),
        migrations.CreateModel(
            name='Tire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.PositiveIntegerField()),
                ('aspect_ratio', models.PositiveIntegerField()),
                ('wheel_size', models.PositiveIntegerField()),
            ],
            options={
                'db_table': 'tires',
            },
        ),
        migrations.CreateModel(
            name='Trim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trimName', models.CharField(max_length=50)),
                ('front_tire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='front_trims', to='cars.tire')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.model')),
                ('rear_tire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rear_trims', to='cars.tire')),
            ],
            options={
                'db_table': 'trims',
            },
        ),
        migrations.CreateModel(
            name='UserTrim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars.trim')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'db_table': 'users_trims',
            },
        ),
        migrations.AddField(
            model_name='trim',
            name='user',
            field=models.ManyToManyField(through='cars.UserTrim', to='users.User'),
        ),
    ]