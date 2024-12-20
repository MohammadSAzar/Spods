# Generated by Django 5.1.1 on 2024-10-18 13:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsorships', '0005_remove_contentmaker_max_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessowner',
            name='general_proposal',
            field=models.FileField(blank=True, null=True, upload_to='BO/general_proposals/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='General Proposal'),
        ),
        migrations.AlterField(
            model_name='contentmaker',
            name='general_proposal',
            field=models.FileField(blank=True, null=True, upload_to='CM/general_proposals/', validators=[django.core.validators.FileExtensionValidator(['pdf'])], verbose_name='General Proposal'),
        ),
    ]
