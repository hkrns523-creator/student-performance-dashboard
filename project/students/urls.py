from django.urls import path
from . import views

# Fix 9: Named URLs
urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add_student, name='add_student'),
    path('update/<int:id>/', views.update_student, name='update_student'),
    path('delete/<int:id>/', views.delete_student, name='delete_student'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
