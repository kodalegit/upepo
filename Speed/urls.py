from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('register', views.register, name='register'),
    path('map', views.map_view, name="map"),
    path('logout', views.logout_view, name="logout"),
    path('documentation', views.docs, name='docs'),
    path('contacts', views.contacts, name='contacts'),
    path('analyze', views.analyze, name="analyze"),
    path('comment', views.comment, name='comment'),
    path('likes/<int:comment_id>', views.likes, name='likes')
]