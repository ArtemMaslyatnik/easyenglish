from rest_framework import serializers
from ee import models


# English
class EnglishSerializer(serializers.ModelSerializer):
    wordbook = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        queryset = models.Wordbook.objects.filter(english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name',
                  'ngsl_number',
                  'transcription',
                  'sound_path',
                  'wordbook']


# New Translate
class EnglishTRranslateSerializer(serializers.ModelSerializer):

    wordbook = serializers.SerializerMethodField()
    verbs = serializers.SerializerMethodField()
    adjectives = serializers.SerializerMethodField()
    nouns = serializers.SerializerMethodField()
    pronouns = serializers.SerializerMethodField()
    prepositions = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        user = self.context['request'].user
        queryset = models.Wordbook.objects.filter(user=user, english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    def get_verbs(self, obj):
        queryset = models.Verb.objects.filter(english=obj)
        return [VerbSerializer(q).data for q in queryset]

    def get_adjectives(self, obj):
        queryset = models.Adjective.objects.filter(english=obj)
        return [AdjectiveSerializer(q).data for q in queryset]

    def get_nouns(self, obj):
        queryset = models.Noun.objects.filter(english=obj)
        return [NounSerializer(q).data for q in queryset]

    def get_pronouns(self, obj):
        queryset = models.Pronoun.objects.filter(english=obj)
        return [PronounSerializer(q).data for q in queryset]

    def get_prepositions(self, obj):
        queryset = models.Preposition.objects.filter(english=obj)
        return [PrepositionSerializer(q).data for q in queryset]

    def get_comments(self, obj):
        queryset = models.Comment.objects.filter(english=obj)
        return [CommentSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name', 'name', 'ngsl_number', 'transcription',
                  'sound_path', 'verbs', 'adjectives', 'nouns', 'pronouns',
                  'prepositions', 'wordbook', 'comments']


# Russian
class RussianSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Russian
        fields = ['id', 'name']


# Adjective
class AdjectiveSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Adjective
        fields = ['id', 'russian', ]


# Adjective translate
class AdjectiveTranslateSerializer(serializers.HyperlinkedModelSerializer):

    wordbook = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        user = self.context['request'].user
        queryset = models.Wordbook.objects.filter(user=user, english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    def get_translate(self, obj):
        queryset = models.Adjective.objects.filter(english=obj)
        return [AdjectiveSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name', 'transcription',
                  'ngsl_number', 'sound_path', 'wordbook', 'translate', ]


# Adverb
class AdverbSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Adverb
        fields = ['id', 'russian', ]


# Adverb translate
class AdverbTranslateSerializer(serializers.HyperlinkedModelSerializer):

    wordbook = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        user = self.context['request'].user
        queryset = models.Wordbook.objects.filter(user=user, english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    def get_translate(self, obj):
        queryset = models.Adverb.objects.filter(english=obj)
        return [AdjectiveSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name', 'transcription',
                  'ngsl_number', 'sound_path', 'wordbook', 'translate', ]


# Conjunction
class ConjunctionSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Conjunction
        fields = ['id', 'russian']


# Conjunction translate
class ConjunctionTranslateSerializer(serializers.HyperlinkedModelSerializer):

    wordbook = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        user = self.context['request'].user
        queryset = models.Wordbook.objects.filter(user=user, english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    def get_translate(self, obj):
        queryset = models.Conjunction.objects.filter(english=obj)
        return [ConjunctionSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name', 'transcription',
                  'ngsl_number', 'sound_path', 'wordbook', 'translate', ]


# Noun
class NounSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Noun
        fields = ['id', 'russian']


# Noun translate
class NounTranslateSerializer(serializers.HyperlinkedModelSerializer):

    wordbook = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        user = self.context['request'].user
        queryset = models.Wordbook.objects.filter(user=user, english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    def get_translate(self, obj):
        queryset = models.Conjunction.objects.filter(english=obj)
        return [NounSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name', 'transcription',
                  'ngsl_number', 'sound_path', 'wordbook', 'translate', ]


# Preposition
class PrepositionSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Preposition
        fields = ['id', 'russian']


# Preposition translate
class PrepositionTranslateSerializer(serializers.HyperlinkedModelSerializer):

    wordbook = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        user = self.context['request'].user
        queryset = models.Wordbook.objects.filter(user=user, english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    def get_translate(self, obj):
        queryset = models.Preposition.objects.filter(english=obj)
        return [NounSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name', 'transcription',
                  'ngsl_number', 'sound_path', 'wordbook', 'translate', ]


# Pronoun
class PronounSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Pronoun
        fields = ['id', 'russian']


# Preposition translate
class PronounTranslateSerializer(serializers.HyperlinkedModelSerializer):

    wordbook = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        user = self.context['request'].user
        queryset = models.Wordbook.objects.filter(user=user, english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    def get_translate(self, obj):
        queryset = models.Pronoun.objects.filter(english=obj)
        return [PronounSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name', 'transcription',
                  'ngsl_number', 'sound_path', 'wordbook', 'translate', ]


# Verb
class VerbSerializer(serializers.HyperlinkedModelSerializer):

    russian = serializers.ReadOnlyField(source='russian.name')

    class Meta:
        model = models.Verb
        fields = ['id', 'russian']


# Verb Translate
class VerbTranslateSerializer(serializers.HyperlinkedModelSerializer):

    wordbook = serializers.SerializerMethodField()
    translate = serializers.SerializerMethodField()

    def get_wordbook(self, obj):
        user = self.context['request'].user
        queryset = models.Wordbook.objects.filter(user=user, english=obj)
        return [WordbookSerializer(q).data for q in queryset]

    def get_translate(self, obj):
        queryset = models.Verb.objects.filter(english=obj)
        return [VerbSerializer(q).data for q in queryset]

    class Meta:
        model = models.English
        fields = ['id', 'name', 'transcription',
                  'ngsl_number', 'sound_path', 'wordbook', 'translate', ]


# Wordbook
class WordbookSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Wordbook
        fields = ['id',]


# Wordbook
class CommentSerializer(serializers.ModelSerializer):

    subcomments = serializers.SerializerMethodField()

    def get_subcomments(self, obj):
        queryset = models.Comment.objects.filter(parent=obj)
        return [CommentSerializer(q).data for q in queryset]

    class Meta:
        model = models.Comment
        fields = ['id', 'text', 'subcomments']
