from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('pub/<int:pub_id>/', views.publication, name="publication"),
    path('user/<int:user_id>/', views.user, name="user"),
    path('submit', views.submit, name="submit"),
    path('logout_view', views.logout_view, name="logout_view"),
    path('login', views.login, name="login"),
]