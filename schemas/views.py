from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Schema, Column
from .forms import ColumnFormSet


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class SchemaCreateView(LoginRequiredMixin, CreateView):
    model = Schema
    fields = ['name', 'column_separator', 'string_character']
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["columns"] = ColumnFormSet(self.request.POST)
        else:
            data["columns"] = ColumnFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        return self.render_to_response(context)


class SchemaUpdateView(LoginRequiredMixin, UpdateView):
    model = Schema
    fields = ['name', 'column_separator', 'string_character']
    success_url = reverse_lazy('list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["columns"] = ColumnFormSet(self.request.POST, instance=self.object)
        else:
            data["columns"] = ColumnFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super().form_valid(form)


class SchemaDeleteView(DeleteView):
    model = Schema
    success_url = reverse_lazy('list')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)
