# Generated by Django 4.2.16 on 2024-11-10 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
