# Generated by Django 3.0.5 on 2020-04-12 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdvanceCartShopping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_product',
            field=models.ManyToManyField(null=True, to='AdvanceCartShopping.Products'),
        ),
    ]
