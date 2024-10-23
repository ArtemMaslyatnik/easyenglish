from django.contrib import admin
from ee.models import Russian, Verb, Adjective, English


@admin.register(Russian)
class RussianAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


# Verb
class VerbInline(admin.TabularInline):
    model = Verb


@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    list_display = ('id', 'english', 'russian')


# Adjective
class AdjectivInline(admin.TabularInline):
    model = Adjective


@admin.register(Adjective)
class AdjectiveAdmin(admin.ModelAdmin):
    list_display = ('id', 'english', 'russian')


# English
@admin.register(English)
class EnglishAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
