from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="schemas/index.html"), name='index'),
    path('create_schema/', views.SchemaCreateView.as_view(), name='create_schema'),
    path('schemas/', views.SchemaListView.as_view(), name='list'),
    path('update_schema/<int:pk>/', views.SchemaUpdateView.as_view(), name='update_schema'),
    path('delete_schema/<int:pk>/', views.SchemaDeleteView.as_view(), name='delete_schema'),
    path('detail_schema/<int:pk>/', views.SchemaDetailView.as_view(), name='detail_schema'),
    path('generate_dataset/', views.generate_dataset, name='generate_dataset'),
]
