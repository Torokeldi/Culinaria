from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe'),
]
