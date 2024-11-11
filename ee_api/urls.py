from django.urls import include, path
from ee_api import views
from rest_framework.routers import DefaultRouter

app_name = 'ee_api'

# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'english', views.EnglishViewSets,
                basename='English')
router.register(r'adjectives', views.AdjectiveTranslateViewSets,
                basename='Adjectives')
router.register(r'adverbs', views.AdverbTranslateViewSets,
                basename='Adverbs')
router.register(r'conjunctions', views.ConjunctionTranslateViewSets,
                basename='Conjunctions')
router.register(r'nouns', views.NounTranslateViewSets,
                basename='Nouns')
router.register(r'prepositions',  views.PrepositionTranslateViewSets,
                basename='Prepositions')
router.register(r'pronouns', views.PronounTranslateViewSets,
                basename='Pronouns')
router.register(r'verbs', views.VerbTranslateViewSets,
                basename='Verbs')
router.register(r'wordbook', views.WordbookViewSets,
                basename='Wordbook')


# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
