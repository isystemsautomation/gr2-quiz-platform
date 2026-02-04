from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('subject/<str:subject>/block/<int:block_number>/', views.block_take, name='block_take'),
    path('subject/<str:subject>/block/<int:block_number>/submit/', views.block_submit, name='block_submit'),
]

