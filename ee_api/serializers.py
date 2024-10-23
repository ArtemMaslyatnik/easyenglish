from rest_framework import serializers
from ee import models


# English
class EnglishSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.English
        fields = ['id', 'name', 'ngsl_number', 'number_of_english']


# Russian
class RussianSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Russian
        fields = ['id', 'name']


# Verb
class VerbSerializer(serializers.HyperlinkedModelSerializer):

    # card_id = serializers.ReadOnlyField(source='card.english.id')
    # englih = serializers.ReadOnlyField(source='card.english.name')
    russian = serializers.ReadOnlyField(source='russian.name')
    # onlt if relation in model
    # russian = RussianSerializer()

    class Meta:
        model = models.Verb
        fields = ['id', 'russian']


# Adjective
class AdjectiveSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Adjective
        fields = ['id', 'russian']


# Noun
class NounSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Noun
        fields = ['id', 'russian']


# Pronoun
class PronounSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Pronoun
        fields = ['id', 'russian']


# Preposition
class PrepositionSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Preposition
        fields = ['id', 'russian']


# New Translate
class CardSerializer(serializers.ModelSerializer):

    verbs = serializers.SerializerMethodField()
    adjectives = serializers.SerializerMethodField()
    nouns = serializers.SerializerMethodField()
    pronouns = serializers.SerializerMethodField()
    prepositions = serializers.SerializerMethodField()

    def get_verbs(self, obj):
        queryset = models.Verb.objects.filter(card=obj)
        return [VerbSerializer(q).data for q in queryset]

    def get_adjectives(self, obj):
        queryset = models.Adjective.objects.filter(card=obj)
        return [AdjectiveSerializer(q).data for q in queryset]

    def get_nouns(self, obj):
        queryset = models.Noun.objects.filter(card=obj)
        return [NounSerializer(q).data for q in queryset]

    def get_pronouns(self, obj):
        queryset = models.Pronoun.objects.filter(card=obj)
        return [PronounSerializer(q).data for q in queryset]

    def get_prepositions(self, obj):
        queryset = models.Preposition.objects.filter(card=obj)
        return [PrepositionSerializer(q).data for q in queryset]

    english = serializers.ReadOnlyField(source='english.name')
    # fields = [field.name for field in model._meta.fields]

    class Meta:
        model = models.English
        fields = ['id', 'english', 'verbs', 'adjectives', 'nouns',
                  'pronouns', 'prepositions']
