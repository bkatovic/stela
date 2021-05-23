from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('candidate/edit/', views.candidate_edit, name='candidate_edit'),
    path('<str:username>/', views.candidate_view, name='candidate_view'),
]
