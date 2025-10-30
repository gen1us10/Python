from django.contrib import admin

from .models import Category, Table, Transaction


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'owner__email')
    list_filter = ('created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'table', 'amount', 'currency', 'date')
    search_fields = ('title', 'table__name', 'table__owner__email')
    list_filter = ('currency', 'date', 'categories')
    ordering = ('-date',)
