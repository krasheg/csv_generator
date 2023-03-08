from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Schema, Column, DataSet
from .forms import ColumnFormSet, DataSetForm


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
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["columns"] = ColumnFormSet(self.request.POST)
        else:
            context["columns"] = ColumnFormSet()
        return context

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
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["columns"] = ColumnFormSet(self.request.POST, instance=self.object)
        else:
            context["columns"] = ColumnFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        columns = context['columns']
        with transaction.atomic():
            self.object = form.save()
            if columns.is_valid():
                columns.instance = self.object
                columns.save()
        return super().form_valid(form)


class SchemaDetailView(LoginRequiredMixin, DetailView):
    model = Schema

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['columns'] = Column.objects.filter(schema_id=self.object.id).select_related()
        context['datasets'] = DataSet.objects.filter(schema_id=self.object.id).select_related()
        if self.request.POST:
            context['create_dataset'] = DataSetForm(self.request.POST)
        else:
            context['create_dataset'] = DataSetForm()
        return context

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return HttpResponseRedirect(
            reverse("detail_schema", kwargs={"pk": self.get_object().pk}))


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    model = Schema
    success_url = reverse_lazy('list')

    def post(self, request, *args, **kwargs):
        if "cancel" in request.POST:
            return HttpResponseRedirect(self.success_url)
        else:
            return super().post(request, *args, **kwargs)


def generate_dataset(request):
    if request.method == 'POST':
        schema_id = request.POST.get('schema_id')
        rows = int(request.POST.get('rows'))
        schema = Schema.objects.get(id=schema_id)
        # Create dataset based on schema
        dataset = DataSet.objects.create(schema=schema, rows=rows)
        count = DataSet.objects.count()
        dataset.save()
        _id = dataset.id
        created_at = dataset.created_at
        dataset.create_csv_file()
        return JsonResponse({'id': _id, 'created_at': created_at, 'count': count})
