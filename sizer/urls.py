from django.urls import path

from sizer import views

urlpatterns = [
    path('photos/', views.PhotoView.as_view()),
    path('photos/<int:photo_id>/', views.PhotoDetailView.as_view()),
    path('photos/<int:photo_id>/download/', views.DownloadImage.as_view()),
    path('photos/<int:photo_id>/zip/', views.DownloadZip.as_view()),
]