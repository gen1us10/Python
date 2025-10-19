from django.conf import settings
from django.db import models


class Table(models.Model):
    """
    Окрема «таблиця витрат» користувача.
    Один користувач може мати кілька таблиць (робота, особисті тощо).
    """
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tables',
    )
    name = models.CharField(max_length=120)
    color = models.CharField(
        max_length=7,
        blank=True,
        default='',
        help_text='Напр. #FF9900',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} ({self.owner.email})'


class Category(models.Model):
    """
    Категорії витрат (створює адмін; прив'язуються до транзакцій).
    """
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """
    Транзакція: сума, валюта, дата, зв'язок з таблицею і (опціонально) категоріями.
    """
    UAH = 'UAH'
    USD = 'USD'
    EUR = 'EUR'
    CURRENCY_CHOICES = [
        (UAH, 'UAH'),
        (USD, 'USD'),
        (EUR, 'EUR'),
    ]

    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='transactions',
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name='transactions',
    )

    title = models.CharField(max_length=150, blank=True, default='')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default=UAH)
    date = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date', '-id')

    def __str__(self):
        return f'{self.amount} {self.currency} [{self.date}]'
