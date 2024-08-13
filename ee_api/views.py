from ee import models
from ee_api import serializers
from rest_framework import viewsets


# EnglishWord
class EnglishViewSets(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = models.English.objects.all()
    serializer_class = serializers.EnglishSerializer


# RussianWord
class RussianViewSets(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = models.Russian.objects.all()
    serializer_class = serializers.RussianSerializer


# New Translate
class CardViewSets(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = models.Card.objects.all()
    serializer_class = serializers.CardSerializer


# Verb Translate
class VerbViewSets(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = models.Verb.objects.all()
    serializer_class = serializers.VerbSerializer
