from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login_user, name='login'),
    path('search', views.search, name='search'),
    path('add', views.add, name='add'),
    path('delete', views.delete_rate, name='delete'),
    path('ports', views.ports, name='ports'),
    path('addPort', views.add_port, name='add_port'),
    path('logout', views.logout_user, name='logout'),
]
