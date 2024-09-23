from django.db import models
from django.contrib.auth.models import User


# Words

class WordLists(models.Model):
    id = models.SmallAutoField
    name = models.CharField(max_length=30, blank=True, default='')
    Wordlist = models.CharField(max_length=30, blank=True, default='')
    WL_SFI_Rank = models.SmallIntegerField()
    RawFreq_Rank = models.IntegerField()


class English(models.Model):

    id = models.SmallAutoField
    name = models.CharField(max_length=30, blank=True, default='')
    ngsl_number = models.SmallIntegerField()
    transcription = models.CharField(max_length=30, blank=True, default='')
    sound_path = models.FileField(upload_to='media/')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    def number_of_english(self):
        return English.objects.all().count()

    # получить данные при сериализации ссылки
    def natural_key(self):
        return (self.name)


class Russian(models.Model):

    id = models.SmallAutoField
    name = models.CharField(max_length=30, blank=True, default='')

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    # получить данные при сериализации ссылки
    def natural_key(self):
        return (self.name)


# Related word
class RelatedEnglishWord(models.Model):

    id = models.SmallAutoField
    name = models.CharField(max_length=30, blank=True, default='')

    # получить данные при сериализации ссылки
    def natural_key(self):
        return (self.name)


# Example
class Example(models.Model):

    id = models.SmallAutoField
    name = models.CharField(max_length=200, blank=True, default='')


# Element
class Card(models.Model):

    id = models.AutoField
    english = models.ForeignKey(English,
                                on_delete=models.CASCADE)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.english.name


# Adjective
class Adjective(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE)
    russian = models.ForeignKey(Russian, on_delete=models.CASCADE)


class AdjectiveCard(models.Model):

    id = models.AutoField
    english = models.ForeignKey(English, on_delete=models.CASCADE)


# Adverb
class Adverb(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE)
    russian = models.ForeignKey(Russian, on_delete=models.CASCADE)


class AdverbCard(models.Model):

    id = models.AutoField
    english = models.ForeignKey(English, on_delete=models.CASCADE)


# Conjunction
class Conjunction(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE
                             )
    russian = models.ForeignKey(Russian,
                                on_delete=models.CASCADE
                                )


class ConjunctionCard(models.Model):

    id = models.AutoField
    english = models.ForeignKey(English,
                                on_delete=models.CASCADE
                                )


# FPoS functional parts of speech
class Fpos(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE
                             )
    russian = models.ForeignKey(Russian,
                                on_delete=models.CASCADE
                                )


# Noun
class Noun(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE
                             )
    russian = models.ForeignKey(Russian,
                                on_delete=models.CASCADE
                                )


class NounCard(models.Model):

    id = models.AutoField
    english = models.ForeignKey(English,
                                on_delete=models.CASCADE
                                )


# Preposition
class Preposition(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE
                             )
    russian = models.ForeignKey(Russian,
                                on_delete=models.CASCADE
                                )


class PrepositionCard(models.Model):

    id = models.AutoField
    english = models.ForeignKey(English,
                                on_delete=models.CASCADE
                                )


# Pronoun
class Pronoun(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE
                             )
    russian = models.ForeignKey(Russian,
                                on_delete=models.CASCADE
                                )


class PronounCard(models.Model):

    id = models.AutoField
    english = models.ForeignKey(English,
                                on_delete=models.CASCADE
                                )


# Verb
class Verb(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE)
    russian = models.ForeignKey(Russian, on_delete=models.CASCADE)


class VerbCard(models.Model):

    id = models.AutoField
    english = models.ForeignKey(English,
                                on_delete=models.CASCADE
                                )


# Related word forms (plural, verb forms)
class RelatedWord(models.Model):

    id = models.AutoField
    card = models.ForeignKey(
                            Card,
                            on_delete=models.CASCADE
                            )
    relate_english_word = models.ForeignKey(
                            RelatedEnglishWord,
                            on_delete=models.CASCADE
                            )


# Exampl word forms
class ExampleWord(models.Model):

    id = models.AutoField
    card = models.ForeignKey(Card,
                             on_delete=models.CASCADE)
    example = models.ForeignKey(Example, on_delete=models.CASCADE)


# Wordbook
class Wordbook(models.Model):
    id = models.AutoField
    english = models.ForeignKey(English,
                                on_delete=models.CASCADE
                                )
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['id']


class Comment(models.Model):

    id = models.AutoField
    created = models.DateTimeField(auto_now_add=True, blank=True)
    active = models.BooleanField(default=True)
    text = models.CharField(max_length=200, blank=True, default='')
    english = models.ForeignKey(English,
                                on_delete=models.CASCADE,
                                null=True
                                )
    user = models.ForeignKey(
                    User,
                    on_delete=models.SET_NULL, null=True, blank=True
                    )
    parent = models.ForeignKey(
                    'self',
                    on_delete=models.CASCADE, null=True,
                    )

    class Meta:
        ordering = ('created',)


# Level
class Level (models.Model):

    id = models.AutoField
    name = models.CharField(max_length=20, blank=True, default='')


# Book
class Book (models.Model):

    id = models.AutoField
    title = models.CharField(max_length=200, blank=True, default='')
    level = models.ForeignKey(Level,
                              on_delete=models.CASCADE,
                              null=True
                              )
    unique_words = models.SmallIntegerField()
    total_words = models.SmallIntegerField()
    description = models.CharField(max_length=1000, blank=True, default='')


class Bookcontent (models.Model):
    id = models.AutoField
    sentence_english = models.CharField(
                                max_length=1000,
                                blank=True,
                                default='')
    sentence_russian = models.CharField(
                                max_length=1000,
                                blank=True,
                                default='')
    book = models.ForeignKey(Book,
                             on_delete=models.CASCADE,
                             null=True
                             )
    page = models.SmallIntegerField(blank=True, null=True)

    chapter = models.BooleanField(null=True)
    chapterName = models.BooleanField(null=True)

    class Meta:
        ordering = ('id',)


# serv rename
class Serv (models.Model):

    id = models.AutoField
    english = models.CharField(max_length=30, blank=True, default='')
    parts_speech = models.CharField(max_length=20, blank=True, default='')
    translate = models.CharField(max_length=500, blank=True, default='')
    transcription_eng = models.CharField(max_length=30, blank=True, default='')
    transcription_use = models.CharField(max_length=30, blank=True, default='')
    sound_path = models.CharField(max_length=50, blank=True, default='')
