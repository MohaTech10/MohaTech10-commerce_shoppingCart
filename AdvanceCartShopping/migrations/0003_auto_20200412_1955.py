# Generated by Django 3.0.5 on 2020-04-12 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdvanceCartShopping', '0002_auto_20200412_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_product',
            field=models.ManyToManyField(blank=True, null=True, to='AdvanceCartShopping.Products'),
        ),
    ]