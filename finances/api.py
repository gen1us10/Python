from django.db.models import Avg, Sum
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Transaction
from .services import convert_to_uah


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def averages_by_category(request):
    """
    Средние траты пользователя по категориям.
    Пример ответа:
    [
      {"categories__name": "Продукти", "currency": "UAH", "avg_amount": 250.5},
      {"categories__name": "Авто", "currency": "EUR", "avg_amount": 33.20},
      ...
    ]
    """
    qs = Transaction.objects.filter(table__owner=request.user)

    data = (
        qs.values('categories__name', 'currency')
          .annotate(avg_amount=Avg('amount'))
          .order_by('categories__name', 'currency')
    )

    return Response(list(data))


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def totals_in_uah(request):
    """
    Общая сумма всех транзакций пользователя, пересчитанная в гривны (UAH).
    Ответ вида:
    {"total_uah": 12345.67}
    """
    qs = Transaction.objects.filter(table__owner=request.user)
    by_cur = qs.values('currency').annotate(total=Sum('amount'))

    total_uah = 0.0
    for row in by_cur:
        amount = float(row['total'])
        currency = row['currency']
        total_uah += convert_to_uah(amount, currency)

    return Response({'total_uah': round(total_uah, 2)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def convert_totals_to_uah(request):
    """
    Возвращает детально:
    {
      "UAH": 2500.00,
      "USD": 20.00,
      "EUR": 35.00,
      "total_uah": 3120.50
    }
    где total_uah — всё пересчитано в гривны.
    """
    qs = Transaction.objects.filter(table__owner=request.user)
    by_cur = qs.values('currency').annotate(total=Sum('amount'))

    payload = {}
    total_uah = 0.0

    for row in by_cur:
        currency = row['currency']
        amount = float(row['total'])
        payload[currency] = round(amount, 2)
        total_uah += convert_to_uah(amount, currency)

    payload['total_uah'] = round(total_uah, 2)

    return Response(payload)
