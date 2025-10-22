from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Table, Transaction
from .forms import TableForm, TransactionForm

class OwnerQuerysetMixin(LoginRequiredMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        if self.model is Table:
            return qs.filter(owner=self.request.user)
        if self.model is Transaction:
            return qs.filter(table__owner=self.request.user)
        return qs.none()

# --- TABLES ---
class TableListView(OwnerQuerysetMixin, ListView):
    model = Table
    template_name = 'finances/table_list.html'

class TableCreateView(LoginRequiredMixin, CreateView):
    model = Table
    form_class = TableForm
    template_name = 'finances/table_form.html'
    success_url = reverse_lazy('finances:table_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TableUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Table
    form_class = TableForm
    template_name = 'finances/table_form.html'
    success_url = reverse_lazy('finances:table_list')

class TableDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Table
    template_name = 'finances/confirm_delete.html'
    success_url = reverse_lazy('finances:table_list')

# --- TRANSACTIONS ---
class TransactionListView(OwnerQuerysetMixin, ListView):
    model = Transaction
    template_name = 'finances/transaction_list.html'
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset().select_related('table').prefetch_related('categories')

        # фильтры
        q = self.request.GET.get('q')         
        day = self.request.GET.get('day')      
        table_id = self.request.GET.get('table')
        category_id = self.request.GET.get('category')

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(table__name__icontains=q))
        if day:
            qs = qs.filter(date=day)
        if table_id:
            qs = qs.filter(table_id=table_id)
        if category_id:
            qs = qs.filter(categories__id=category_id)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user

       
        ctx['tables'] = Table.objects.filter(owner=user)
        totals = self.get_queryset().values('currency').annotate(total=Sum('amount'))
        ctx['totals_by_currency'] = list(totals)
        return ctx

class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('finances:transaction_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['table'].queryset = Table.objects.filter(owner=self.request.user)
        return form

class TransactionUpdateView(OwnerQuerysetMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = 'finances/transaction_form.html'
    success_url = reverse_lazy('finances:transaction_list')

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['table'].queryset = Table.objects.filter(owner=self.request.user)
        return form

class TransactionDeleteView(OwnerQuerysetMixin, DeleteView):
    model = Transaction
    template_name = 'finances/confirm_delete.html'
    success_url = reverse_lazy('finances:transaction_list')
