from django.urls import path
from . import views

urlpatterns = [
    path('',views.video_upload_view, name='home'),
]
