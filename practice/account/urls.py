from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name = 'login'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('register/', views.register, name = 'register'),
    path('edituser/<int:user_id>', views.edituser, name = 'edituser'),
    path('viewuser/<int:user_id>', views.viewuser, name = 'viewuser'),
    path('updateuser/<int:user_id>', views.updateuser, name = 'updateuser'),
    path('deleteuser/<int:user_id>', views.deleteuser, name = 'deleteuser'),
    path('logout/', views.logout, name = 'logout'),
]