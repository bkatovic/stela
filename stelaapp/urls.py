from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('results/', views.election_results, name="election_results"),
    path('candidate/edit/', views.candidate_edit, name='candidate_edit'),
    path('<str:username>/', views.candidate_view, name='candidate_view'),
    path('<str:username>/vote', views.vote, name='candidate_view'),
    path('<str:username>/unvote', views.unvote, name='candidate_view'),
]
