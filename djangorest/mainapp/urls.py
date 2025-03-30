from django.urls import path
from rest_framework import routers
from mainapp import views

router = routers.DefaultRouter()
#router.register('menu', views.MenuItemViewSet)

urlpatterns = [
    path('song/', views.get_song),
]