from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('add/', views.add_student),
    path('update/<int:id>/', views.update_student),
    path('delete/<int:id>/', views.delete_student),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
]