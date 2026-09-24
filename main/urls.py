from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe'),
    path( 'login/', views.login_view, name='login' ),
    path( 'register/', views.register_view, name='register' ),
    path( 'logout/', views.logout_view, name='logout' ),
    path("categories/", views.categories, name="categories"),
    path("add_recipe/", views.add_recipe, name="add_recipe"),
    path('profile/', views.profile, name='profile'),
]
