# Generated by Django 5.1 on 2024-08-25 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=10)),
                ('quantity', models.IntegerField()),
                ('order_type', models.CharField(choices=[('MKT', 'Market Order'), ('LMT', 'Limit Order')], max_length=3)),
                ('buy_or_sell', models.CharField(choices=[('B', 'Buy'), ('S', 'Sell')], max_length=1)),
                ('exchange', models.CharField(choices=[('NSE', 'National Stock Exchange'), ('BSE', 'Bombay Stock Exchange')], max_length=3)),
                ('product_type', models.CharField(choices=[('C', 'Delivery'), ('I', 'Intraday')], max_length=1)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
