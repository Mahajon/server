# Generated by Django 4.2.11 on 2024-04-15 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_category_slug_alter_subcategory_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
