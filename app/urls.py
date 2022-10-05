from django.urls import path
from . import views

urlpatterns = [
    path('', views.chice , name="chice"),
    path('<int:question_id>/detail/', views.detail, name='detail'),
    path('home/', views.Home.as_view(), name='home'),
]

