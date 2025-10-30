from django.urls import path

from . import api

app_name = 'api'

urlpatterns = [
    path('analytics/avg-by-category/', api.averages_by_category, name='avg_by_category'),
    path('analytics/totals-in-uah/', api.totals_in_uah, name='totals_in_uah'),
    path('analytics/convert-totals-to-uah/', api.convert_totals_to_uah, name='convert_totals_to_uah'),
]
