# Generated by Django 3.2 on 2021-04-24 09:59

from django.db import migrations, models # pragma: no cover



class Migration(migrations.Migration): # pragma: no cover

    dependencies = [
        ('api', '0002_stock_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='purchase_date',
            field=models.DateTimeField(verbose_name='data purchase this stock.'),
        ),
        migrations.AlterUniqueTogether(
            name='stock',
            unique_together={('user', 'code')},
        ),
    ]
