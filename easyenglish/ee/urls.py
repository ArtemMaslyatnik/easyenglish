from django.urls import path
from ee import views, general_purpose

app_name = 'ee'

urlpatterns = [
     path('',
          views.index,
          name=''),
     path('index',
          views.index,
          name='index'),
     path('english_words/',
          views.EnglishWordListView.as_view(),
          name='english_words'),
     path('word/<int:pk>/',
          views.WordDetailView.as_view(),
          name='word_detail'),
     path('adjectives/',
          views.AdjectiveListView.as_view(),
          name='adjectives'),
     path('adverbs/',
          views.AdverbListView.as_view(),
          name='adverbs'),
     path('conjunctions/',
          views.ConjunctionListView.as_view(),
          name='conjunctions'),
     path('nouns/',
          views.NounListView.as_view(),
          name='nouns'),
     path('pronouns/',
          views.PronounListView.as_view(),
          name='pronouns'),
     path('prepositions/',
          views.PrepositionListView.as_view(),
          name='prepositions'),
     path('verbs/',
          views.VerbListView.as_view(),
          name='verbs'),
     path('universal/',
          views.universal,
          name='universal'),
     path('text_analysis/',
          views.TextAnalysis,
          name='text_analysis'),
     path('import/',
          general_purpose.import_from_excel,
          name='import_from_excel'),
     # path('export/',
     #      views.export_excel,
     #      name='export_excel'),
     # path('alter/',
     #      views.alter_dic,
     #      name='alter_dic'),
     # path("upload-file/",
     #      views.upload_file,
     #      name="upload-file"),
     path('wordbook/',
          views.WordbookListView.as_view(),
          name='wordbook_list'),
     path('wordbook/<int:pk>/',
          views.WordbookDetailView.as_view(),
          name='wordbook_detail'),
     path('book/',
          views.BookListView.as_view(),
          name='book_list'),
     path('book/<int:pk>/page/<int:page>/',
          views.BookDetailView.as_view(),
          name='book_detail'),
     path('book/translate/',
          views.BookDetailView().translate,
          name='book_translate'),
     path('book/translateWord/',
          views.BookDetailView().translateWord,
          name='book_translate_word'),
     path('comment/create/<int:pk>/',
          views.Comment().create,
          name='create_comment'),
     path('wordbook/create/<int:pk>/',
          views.WordbookListView().create,
          name='create_wordbook'),
]
