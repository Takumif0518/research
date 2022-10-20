from django.urls import path
from . import views

urlpatterns = [
    path('', views.choice , name="choice"),
    path('<int:question_id>/detail/', views.detail, name='detail'),
    path('home/', views.Home.as_view(), name='home'),
    #path('teacher', views.teacher , name="teacher"),
]

