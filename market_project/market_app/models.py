from django.db import models

# Create your models here.
class Order(models.Model):
    ORDER_TYPES = [
        ('MKT', 'Market Order'),
        ('LMT', 'Limit Order'),
    ]

    BUY_SELL_CHOICES = [
        ('B', 'Buy'),
        ('S', 'Sell'),
    ]

    EXCHANGES = [
        ('NSE', 'National Stock Exchange'),
        ('BSE', 'Bombay Stock Exchange'),
    ]

    PRODUCT_TYPES = [
        ('C', 'Delivery'),
        ('I', 'Intraday'),
    ]

    symbol = models.CharField(max_length=10)
    quantity = models.IntegerField()
    order_type = models.CharField(max_length=3, choices=ORDER_TYPES)
    buy_or_sell = models.CharField(max_length=1, choices=BUY_SELL_CHOICES)
    exchange = models.CharField(max_length=3, choices=EXCHANGES)
    product_type = models.CharField(max_length=1, choices=PRODUCT_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.buy_or_sell} {self.symbol} - {self.quantity} @ {self.price if self.price else 'Market'} ({self.exchange})"
