# Generated by Django 3.2.7 on 2021-12-01 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='notes',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]