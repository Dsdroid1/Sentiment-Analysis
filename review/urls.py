from django.urls import path
from . import views

urlpatterns = [
    path('review_it/',views.review_process,name="review"),
    path('form/',views.form,name='form'),
    path('movie/',views.movieData,name='movie'),
    path('movielist/',views.updateReviews,name='reviewIT')
]