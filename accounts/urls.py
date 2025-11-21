from django.urls import path

from . import views

urlpatterns = [
    path('', views.user_management, name='user_management'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('creditos/', views.credits_view, name='credits'),
    path('eliminar/', views.delete_user, name='delete_user'),
]
