from ee import models
from ee_api import serializers
from ee_api.permission import ReadOnly

from rest_framework import viewsets


# EnglishWord
class EnglishViewSets(viewsets.ModelViewSet):
    queryset = models.English.objects.all()
    serializer_class = serializers.EnglishTRranslateSerializer
    permission_classes = (ReadOnly, )


# RussianWord
class RussianViewSets(viewsets.ModelViewSet):

    queryset = models.Russian.objects.all()
    serializer_class = serializers.RussianSerializer
    permission_classes = (ReadOnly, )


# Adjective
class AdjectiveTranslateViewSets(viewsets.ModelViewSet):

    query_text = (' SELECT eng.id'
                  ' FROM ee_english  eng'
                  ' INNER JOIN ee_adjective ON eng.id '
                  ' = ee_Adjective.english_id'
                  ' GROUP BY eng.id'
                  ' ORDER BY eng.id')

    serializer_class = serializers.AdjectiveTranslateSerializer
    queryset = models.English.objects.raw(query_text)
    permission_classes = (ReadOnly, )


# Adverb
class AdverbTranslateViewSets(viewsets.ModelViewSet):

    query_text = (' SELECT eng.id'
                  ' FROM ee_english  eng'
                  ' INNER JOIN ee_adverb ON eng.id '
                  ' = ee_adverb.english_id'
                  ' GROUP BY eng.id'
                  ' ORDER BY eng.id')

    serializer_class = serializers.AdjectiveTranslateSerializer
    queryset = models.English.objects.raw(query_text)
    permission_classes = (ReadOnly, )


# Conjunction
class ConjunctionTranslateViewSets(viewsets.ModelViewSet):

    query_text = (' SELECT eng.id'
                  ' FROM ee_english  eng'
                  ' INNER JOIN ee_conjunction ON eng.id '
                  ' = ee_conjunction.english_id'
                  ' GROUP BY eng.id'
                  ' ORDER BY eng.id')

    serializer_class = serializers.ConjunctionTranslateSerializer
    queryset = models.English.objects.raw(query_text)
    permission_classes = (ReadOnly, )


# Noun
class NounTranslateViewSets(viewsets.ModelViewSet):

    query_text = (' SELECT eng.id'
                  ' FROM ee_english  eng'
                  ' INNER JOIN ee_noun ON eng.id '
                  ' = ee_noun.english_id'
                  ' GROUP BY eng.id'
                  ' ORDER BY eng.id')

    serializer_class = serializers.NounTranslateSerializer
    queryset = models.English.objects.raw(query_text)
    permission_classes = (ReadOnly, )


# Noun
class PrepositionTranslateViewSets(viewsets.ModelViewSet):

    query_text = (' SELECT eng.id'
                  ' FROM ee_english  eng'
                  ' INNER JOIN ee_preposition ON eng.id '
                  ' = ee_preposition.english_id'
                  ' GROUP BY eng.id'
                  ' ORDER BY eng.id')

    serializer_class = serializers.PrepositionTranslateSerializer
    queryset = models.English.objects.raw(query_text)
    permission_classes = (ReadOnly, )


# Noun
class PronounTranslateViewSets(viewsets.ModelViewSet):

    query_text = (' SELECT eng.id'
                  ' FROM ee_english  eng'
                  ' INNER JOIN ee_pronoun ON eng.id '
                  ' = ee_pronoun.english_id'
                  ' GROUP BY eng.id'
                  ' ORDER BY eng.id')

    serializer_class = serializers.PronounTranslateSerializer
    queryset = models.English.objects.raw(query_text)
    permission_classes = (ReadOnly, )


# Verb
class VerbTranslateViewSets(viewsets.ModelViewSet):

    query_text = (' SELECT eng.id'
                  ' FROM ee_english  eng'
                  ' INNER JOIN ee_verb ON eng.id  = ee_verb.english_id'
                  ' GROUP BY eng.id'
                  ' ORDER BY eng.id')

    serializer_class = serializers.VerbTranslateSerializer
    queryset = models.English.objects.raw(query_text)
    permission_classes = (ReadOnly, )


# # Wordbook
# class WordbookViewSets(viewsets.ModelViewSet):

#     serializer_class = serializers.WordbookSerializer

#     def get_queryset(self):
#         user = self.request.user
#         return models.Wordbook.objects.filter(user=user)
#     permission_classes = (IsOwnerOrReadOnly, )

# Wordbook
class WordbookViewSets(viewsets.ModelViewSet):

    query_text = (' SELECT eng.id'
                  ' FROM ee_english  eng'
                  ' INNER JOIN ee_wordbook ON eng.id  = ee_wordbook.english_id'
                  ' WHERE ee_wordbook.user_id = %s'
                  ' GROUP BY eng.id'
                  ' ORDER BY eng.id')

    serializer_class = serializers.EnglishTRranslateSerializer

    def get_queryset(self):
        return models.English.objects.raw(self.query_text,
                                          [self.request.user.id])

    # permission_classes = (IsOwnerOrReadOnly, )
