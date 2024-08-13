from django.urls import include, path
from ee_api import views
from rest_framework.routers import DefaultRouter

app_name = 'ee_api'

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'english', views.EnglishViewSets, basename="English")
router.register(r'russian', views.RussianViewSets, basename="Russian")
router.register(r'card', views.CardViewSets, basename="Card")
router.register(r'verb', views.VerbViewSets, basename="Verb")


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
