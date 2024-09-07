from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home_view, name="home"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('resource_dashboard/', views.resource_dashboard, name='resource_dashboard'),
    path('manager_dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_form/', views.user_create_view, name='user_form'),
    path('user_list/', views.user_view, name="user_list"),
    path('update/<int:user_id>/', views.update_view, name="doc_update"),
    path('delete/<int:user_id>/', views.delete_view, name="doc_delete"),
]