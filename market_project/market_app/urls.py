from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('get_indices_prices/', views.get_indices_prices, name='get_indices_prices'),

]
