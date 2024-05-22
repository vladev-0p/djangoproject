from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('', views.browse, name='browse'),
    path('<int:pk>/', views.detail, name='detail'),
    path('new/', views.new_product, name='new'),
    path('<int:pk>/edit/', views.edit_product, name='edit'),
    path('<int:pk>/delete/', views.delete_product, name='delete'),
]
