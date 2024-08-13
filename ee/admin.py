from django.contrib import admin
from ee.models import AdjectiveCard, Card, Russian, Verb, Adjective, VerbCard


@admin.register(Russian)
class RussianAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Verb
class VerbInline(admin.TabularInline):
    model = Verb


@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'russian')


@admin.register(VerbCard)
class VerbCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'english')


# Adjective
class AdjectivInline(admin.TabularInline):
    model = Adjective


@admin.register(Adjective)
class AdjectiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'russian')


@admin.register(AdjectiveCard)
class AdjectiveCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'english')


# Card
@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'english')
    inlines = [VerbInline, AdjectivInline]
