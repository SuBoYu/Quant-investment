from django.contrib import admin
from django.urls import path
from DjangoWeb import views

urlpatterns = [
    path('admin/', admin.site.urls), path('fuckyouasshole/', views.index)
]
