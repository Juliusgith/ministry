# Generated by Django 5.0.6 on 2024-11-17 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Ministry', '0003_uploadrequest_alter_donation_item_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadedform',
            name='admin_reply',
            field=models.TextField(blank=True, help_text='Write your reply here', null=True),
        ),
        migrations.AddField(
            model_name='uploadedform',
            name='is_replied',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='uploadedform',
            name='replied_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
