
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name = 'login_page'),
    path('signup', views.signup_page, name = 'signup_page'),
    path('home', views.home_page, name='home_page'),
    path('logout', views.logout_page, name='logout_page'),
    path('custom_admin', views.custom_admin, name='custom_admin'),
    path('login', views.login_page, name = 'login_page'),
    path('add', views.add, name = 'add'),
    path('edit', views.edit, name = 'edit'),
    path('update/<str:id>', views.update, name = 'update'),  #we give id in html update section
    path('delete/<str:id>', views.delete, name = 'delete'),
    path('admin_login', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name= 'admin_logout'),
    path('admin_search', views.admin_search, name='admin_search'),
    
]