# Generated by Django 5.1.1 on 2024-10-24 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestContentMaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('creator', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500)),
                ('cover', models.ImageField(upload_to='podcast_covers/')),
                ('subscribers', models.PositiveBigIntegerField()),
                ('played', models.PositiveBigIntegerField()),
            ],
        ),
    ]