from django.urls import path
from ee import views


app_name = 'ee'

urlpatterns = [
    # Для статики????
    # path('', TemplateView.as_view(template_name="ee/templates/index.html")),
    # path('index/',
    # TemplateView.as_view(template_name="ee/templates/index.html")),
    path('index',
         views.index,
         name='index'
         ),
    path('universal/',
         views.universal,
         name='universal'
         ),
    path('content/',
         views.get_content,
         name='get_content'
         ),
    path('import/',
         views.import_from_excel,
         name='import_from_excel'
         ),
    path('export/',
         views.export_excel,
         name='export_excel'
         ),
    path('alter/',
         views.alter_dic,
         name='alter_dic'
         ),
    path("upload-file/",
         views.upload_file,
         name="upload-file"),
    path('comment/create/<int:pk>/',
         views.Comment().create,
         name='create_comment'),
    path('wordbook/create/<int:pk>/',
         views.WordbookListView().create,
         name='create_wordbook'),
    path('cards/',
         views.CardListView.as_view(),
         name='card_list'),
    path('card/<int:pk>/',
         views.CardDetailView.as_view(),
         name='card_detail'),
    path('wordbook/',
         views.WordbookListView.as_view(),
         name='wordbook_list'),
    path('wordbook/<int:pk>/',
         views.WordbookDetailView.as_view(),
         name='wordbook_detail'),
    path('book/',
         views.BookListView.as_view(),
         name='book_list'),
    path('book/<int:pk>/page/<int:page>',
         views.BookDetailView.as_view(),
         name='book_detail'),
    path('book/translate/',
         views.BookDetailView().translate,
         name='book_translate'),
    path('book/translateWord/',
         views.BookDetailView().translateWord,
         name='book_translate_word'),
    path('adjective_cards/',
         views.AdjectiveCardListView.as_view(),
         name='adjective_card_list'
         ),
    path('adjective_card/<int:pk>/',
         views.AdjectiveCardDetailView.as_view(),
         name='adjective_card_detail'
         ),
    path('adverb_cards/',
         views.AdverbCardListView.as_view(),
         name='adverb_card_list'
         ),
    path('adverb_card/<int:pk>/',
         views.AdverbCardDetailView.as_view(),
         name='adverb_card_detail'
         ),
    path('conjunction_cards/',
         views.ConjunctionCardListView.as_view(),
         name='conjunction_card_list'
         ),
    path('conjunction_card/<int:pk>/',
         views.ConjunctionCardDetailView.as_view(),
         name='conjunction_card_detail'
         ),
    path('noun_cards/',
         views.NounCardListView.as_view(),
         name='noun_card_list'
         ),
    path('noun_card/<int:pk>/',
         views.NounCardDetailView.as_view(),
         name='noun_card_detail'
         ),
    path('pronoun_cards/',
         views.PronounCardListView.as_view(),
         name='pronoun_card_list'
         ),
    path('pronoun_card/<int:pk>/',
         views.PronounCardDetailView.as_view(),
         name='pronoun_card_detail'
         ),
    path('preposition_cards/',
         views.PrepositionCardListView.as_view(),
         name='preposition_card_list'
         ),
    path('preposition_card/<int:pk>/',
         views.PrepositionCardDetailView.as_view(),
         name='preposition_card_detail'
         ),
    path('verb_cards/',
         views.VerbCardListView.as_view(),
         name='verb_card_list'
         ),
    path('verb_card/<int:pk>/',
         views.VerbCardDetailView.as_view(),
         name='verb_card_detail'
         ),
    # test
    path('english/',
         views.EnglishListView.as_view(),
         name='english_list'
         ),
]


