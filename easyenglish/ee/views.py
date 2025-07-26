import json
import re
import string
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from config import settings
from ee import models, forms
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.serializers import serialize
from django.contrib.auth import logout, login
from ee.general_purpose import text_analysisWord, alter_dic, export_excel, get_content, import_from_excel, set_sound_path


# Create your views here.
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits+1

    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(
        request,
        'index.html',
    )


def logout_view(request):

    logout(request)

    return render(
        request,
        'index.html',
    )


def login_view(request):

    login(request, user)

    return render(
        request,
        'index.html',
    )


# English
class EnglishWordListView(generic.ListView):
    query_text = ('SELECT *, (SELECT english_id FROM ee_wordbook '
                  ' WHERE ee_wordbook.english_id = ee_english.id '
                  ' AND ee_wordbook.user_id = %s) AS word '
                  ' FROM ee_english '
                  ' ORDER BY id ')

    template_name = 'Lists/list.html'
    context_object_name = 'list_english'
    model = models.English
    paginate_by = 20

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.raw(self.query_text, [self.request.user.id])

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(EnglishWordListView, self).get_context_data(**kwargs)

        context['title'] = 'Слова по релевантности'
        context['url_word'] = 'ee:word_detail'
        context['url_create_word'] = 'ee:create_wordbook'
        context['inf'] = 'Нет слов'
        return context


# English word
class WordDetailView(generic.DetailView):
    template_name = 'Word/word_detail.html'
    model = models.English
    context_object_name = 'detail'

    # def getComments(self):
    #     SetComments = models.Comment.objects.all().filter(
    #         english=self.object
    #     )
    #     listComment = []
    #     for item in SetComments:
    #         strComment = {'id': item.id,
    #                       'text': item.text,
    #                       'user': item.user,
    #                       'created': item.created,
    #                       'active': item.active,
    #                       'subComment': models.Comment.objects.all().filter(
    #                           parent_id=item.id
    #                       )
    #                       }
    #         listComment.append(strComment)
    #     return listComment

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context.update({
            'adjective_list': models.Adjective.objects.all().filter(
                english=self.object),
            'adverb_list': models.Adverb.objects.all().filter(
                english=self.object),
            'conjunction_list': models.Conjunction.objects.all().filter(
                english=self.object),
            'fpos_list': models.Fpos.objects.all().filter(
                english=self.object),
            'noun_list': models.Noun.objects.all().filter(
                english=self.object),
            'preposition_list': models.Preposition.objects.all().filter(
                english=self.object),
            'pronoun_list': models.Pronoun.objects.all().filter(
                english=self.object),
            'related_list': models.RelatedWord.objects.all().filter(
                english=self.object),
            'verb_list': models.Verb.objects.all().filter(
                english=self.object),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object,
                user_id=self.request.user.id),
            'comments': getComments(self.object),
            'next': models.English.objects.all().filter(
                id__gt=self.object.id
            ).order_by('id').first(),
            'previous': models.English.objects.all().filter(
                id__lt=self.object.id
            ).order_by('id').last(),
            'title': 'Слова по релевантности',
            'url_list': 'ee:english_words',
            'url_word': 'ee:word_detail',
            'url_create_word': 'ee:create_wordbook',
            'default_image': settings.DEFAULT_USER_IMAGE,
        })

        return context


# Adjective
class AdjectiveListView(generic.ListView):

    query_text = ('SELECT 1 id, row_number() OVER(ORDER BY english_id) '
                  ' number_row, english_id, eng.name, NULL rus_id, '
                  ' NULL rus, eng.transcription, eng.sound_path, '
                  ' (SELECT english_id FROM ee_wordbook '
                  ' WHERE ee_wordbook.english_id = ee_adjective.english_id '
                  ' AND ee_wordbook.user_id = %s) AS word '
                  ' FROM ee_adjective '
                  ' LEFT JOIN ee_english eng ON english_id = eng.id'
                  ' GROUP BY english_id, eng.name , eng.transcription, '
                  ' eng.sound_path'
                  ' UNION SELECT 1, NULL, english_id,  NULL, russian_id, '
                  '     ee_russian.name, NULL, NULL, NULL'
                  ' FROM ee_adjective'
                  ' LEFT JOIN ee_russian ON russian_id = ee_russian.id'
                  ' ORDER BY english_id, number_row')

    template_name = 'Lists/list.html'
    context_object_name = 'list'
    model = models.Adjective
    paginate_by = 40

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.raw(self.query_text, [self.request.user.id])

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(AdjectiveListView, self).get_context_data(**kwargs)

        context['title'] = 'Прилагательные'
        context['inf'] = 'Нет слов'

        return context


# Adverb
class AdverbListView(generic.ListView):

    query_text = ('SELECT 1 id, row_number() OVER(ORDER BY english_id) '
                  ' number_row, english_id, eng.name, NULL rus_id, NULL rus, '
                  ' eng.transcription, eng.sound_path, '
                  ' (SELECT english_id FROM ee_wordbook '
                  ' WHERE ee_wordbook.english_id = ee_adverb.english_id '
                  ' AND ee_wordbook.user_id = %s) AS word '
                  ' FROM ee_adverb '
                  ' LEFT JOIN ee_english eng ON english_id = eng.id'
                  ' GROUP BY english_id, eng.name , eng.transcription, '
                  ' eng.sound_path '
                  ' UNION SELECT 1, NULL, english_id,  NULL, russian_id, '
                  ' ee_russian.name, NULL, NULL, NULL '
                  ' FROM ee_adverb'
                  ' LEFT JOIN ee_russian ON russian_id = ee_russian.id'
                  ' ORDER BY english_id, number_row')

    template_name = 'Lists/list.html'
    context_object_name = 'list'
    model = models.Adverb
    paginate_by = 40

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.raw(self.query_text, [self.request.user.id])

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(AdverbListView, self).get_context_data(**kwargs)
        context['title'] = 'Наречия'
        context['inf'] = 'Нет слов'

        return context


# Conjunction
class ConjunctionListView(generic.ListView):

    query_text = (
        'SELECT 1 id, row_number() OVER(ORDER BY english_id) number_row,'
        ' english_id, eng.name, NULL rus_id, NULL rus, eng.transcription, '
        ' eng.sound_path, '
        ' (SELECT english_id FROM ee_wordbook '
        ' WHERE ee_wordbook.english_id = ee_conjunction.english_id '
        ' AND ee_wordbook.user_id = %s) AS word '
        ' FROM ee_conjunction '
        ' LEFT JOIN ee_english eng ON english_id = eng.id'
        ' GROUP BY english_id, eng.name , eng.transcription, eng.sound_path'
        ' UNION SELECT 1, NULL, english_id,  NULL, russian_id, '
        ' ee_russian.name, NULL, NULL, NULL '
        ' FROM ee_conjunction'
        ' LEFT JOIN ee_russian ON russian_id = ee_russian.id'
        ' ORDER BY english_id, number_row')

    template_name = 'Lists/list.html'
    model = models.Conjunction
    context_object_name = 'list'
    paginate_by = 40

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.raw(self.query_text, [self.request.user.id])

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(ConjunctionListView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Союзы'
        context['inf'] = 'Нет слов'

        return context


# Noun
class NounListView(generic.ListView):

    query_text = (
        'SELECT 1 id, row_number() OVER(ORDER BY english_id) number_row,'
        ' english_id, eng.name, NULL rus_id, NULL rus, eng.transcription, '
        ' eng.sound_path, '
        ' (SELECT english_id FROM ee_wordbook '
        ' WHERE ee_wordbook.english_id = ee_noun.english_id '
        ' AND ee_wordbook.user_id = %s) AS word '
        ' FROM ee_noun '
        ' LEFT JOIN ee_english eng ON english_id = eng.id'
        ' GROUP BY english_id, eng.name , eng.transcription, eng.sound_path'
        ' UNION SELECT 1, NULL, english_id,  NULL, russian_id, '
        ' ee_russian.name, NULL, NULL, NULL'
        ' FROM ee_noun'
        ' LEFT JOIN ee_russian ON russian_id = ee_russian.id'
        ' ORDER BY english_id, number_row')

    template_name = 'Lists/list.html'
    model = models.Noun
    context_object_name = 'list'
    paginate_by = 40

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.raw(self.query_text, [self.request.user.id])

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(NounListView, self).get_context_data(**kwargs)

        context['title'] = 'Существительные'
        context['inf'] = 'Нет слов'
        return context


# Preposition
class PrepositionListView(generic.ListView):

    query_text = (
        'SELECT 1 id, row_number() OVER(ORDER BY english_id) number_row,'
        ' english_id, eng.name, NULL rus_id, NULL rus, eng.transcription, '
        ' eng.sound_path, '
        ' (SELECT english_id FROM ee_wordbook '
        ' WHERE ee_wordbook.english_id = ee_preposition.english_id '
        ' AND ee_wordbook.user_id = %s) AS word '
        ' FROM ee_preposition '
        ' LEFT JOIN ee_english eng ON english_id = eng.id'
        ' GROUP BY english_id, eng.name , eng.transcription, eng.sound_path'
        ' UNION SELECT 1, NULL, english_id,  NULL, russian_id, '
        ' ee_russian.name, NULL, NULL , NULL '
        ' FROM ee_preposition'
        ' LEFT JOIN ee_russian ON russian_id = ee_russian.id'
        ' ORDER BY english_id, number_row')

    template_name = 'Lists/list.html'
    model = models.Preposition
    context_object_name = 'list'
    paginate_by = 40

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.raw(self.query_text, [self.request.user.id])

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(PrepositionListView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Предлоги'
        context['inf'] = 'Нет слов'
        return context


# Pronoun
class PronounListView(generic.ListView):

    query_text = (
        'SELECT 1 id, row_number() OVER(ORDER BY english_id) number_row,'
        ' english_id, eng.name, NULL rus_id, NULL rus, '
        ' eng.transcription, eng.sound_path, '
        ' (SELECT english_id FROM ee_wordbook '
        ' WHERE ee_wordbook.english_id = ee_pronoun.english_id '
        ' AND ee_wordbook.user_id = %s) AS word '
        ' FROM ee_pronoun '
        ' LEFT JOIN ee_english eng ON english_id = eng.id'
        ' GROUP BY english_id, eng.name , eng.transcription, eng.sound_path'
        ' UNION SELECT 1, NULL, english_id,  NULL, russian_id, '
        ' ee_russian.name, NULL, NULL, NULL'
        ' FROM ee_pronoun'
        ' LEFT JOIN ee_russian ON russian_id = ee_russian.id'
        ' ORDER BY english_id, number_row')

    template_name = 'Lists/list.html'
    model = models.Pronoun
    context_object_name = 'list'
    paginate_by = 40

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.raw(self.query_text, [self.request.user.id])

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(PronounListView, self).get_context_data(**kwargs)

        context['title'] = 'Местоимения'
        context['inf'] = 'Нет слов'
        return context


# Verb
class VerbListView(generic.ListView):

    query_text = (
        'SELECT 1 id, row_number() OVER(ORDER BY english_id) number_row,'
        ' english_id, eng.name, NULL rus_id, NULL rus, '
        ' eng.transcription, eng.sound_path, '
        ' (SELECT english_id FROM ee_wordbook '
        ' WHERE ee_wordbook.english_id = ee_verb.english_id '
        ' AND ee_wordbook.user_id = %s) AS word '
        ' FROM ee_verb '
        ' LEFT JOIN ee_english eng ON english_id = eng.id'
        ' GROUP BY english_id, eng.name , eng.transcription, eng.sound_path'
        ' UNION SELECT 1, NULL, english_id,  NULL, russian_id, '
        ' ee_russian.name, NULL, NULL, NULL'
        ' FROM ee_verb'
        ' LEFT JOIN ee_russian ON russian_id = ee_russian.id'
        ' ORDER BY english_id, number_row')

    template_name = 'Lists/list.html'
    context_object_name = 'list'
    model = models.Verb
    paginate_by = 40

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.raw(self.query_text, [self.request.user.id])

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(VerbListView, self).get_context_data(**kwargs)

        context['title'] = 'Глаголы'
        context['inf'] = 'Нет слов'
        return context


# Wordbook
class WordbookListView(LoginRequiredMixin, generic.ListView):

    template_name = 'Wordbook/wordbook.html'
    model = models.Wordbook
    context_object_name = 'wordbook'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user_id=self.request.user.id)

    def create(self, request, pk):

        if request.method == "POST" and self.is_ajax(request):
            id_word = request.POST.get('path')
            wordbook = request.POST.get('wordbook')
            # chek for list
            querySet = models.Wordbook.objects.filter(
                    english_id=id_word,
                    user_id=request.user.id)
            if querySet.count() > 0:
                querySet.delete()
                response = {
                    'wordbook_list': False,
                    'id': id_word,
                    'wordbook': wordbook}
            else:
                models.Wordbook.objects.create(
                    english_id=id_word,
                    user_id=request.user.id)
                response = {
                    'wordbook_list': True,
                    'id': id_word}
        return JsonResponse(response)

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(WordbookListView, self).get_context_data(**kwargs)

        context['title'] = 'Словарик'
        context['url_word'] = 'ee:wordbook_detail'
        context['url_create_word'] = 'ee:create_wordbook'
        context['inf'] = 'Нет слов'
        return context


class WordbookDetailView(LoginRequiredMixin, generic.DetailView):

    template_name = 'Wordbook/wordbook_detail.html'
    model = models.Wordbook
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context.update({
            'adjective_list': models.Adjective.objects.all().filter(
                english=self.object.english),
            'adverb_list': models.Adverb.objects.all().filter(
                english=self.object.english),
            'conjunction_list': models.Conjunction.objects.all().filter(
                english=self.object.english),
            'fpos_list': models.Fpos.objects.all().filter(
                english=self.object.english),
            'noun_list': models.Noun.objects.all().filter(
                english=self.object.english),
            'preposition_list': models.Preposition.objects.all().filter(
                english=self.object.english),
            'pronoun_list': models.Pronoun.objects.all().filter(
                english=self.object.english),
            'related_list': models.RelatedWord.objects.all().filter(
                english=self.object.english),
            'verb_list': models.Verb.objects.all().filter(
                english=self.object.english),
            'wordbook_list': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            'comments': getComments(self.object.english),
            'next': models.Wordbook.objects.all().filter(
                user_id=self.request.user.id,
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.Wordbook.objects.all().filter(
                user_id=self.request.user.id,
                english__lt=self.object.english
            ).order_by('english').last(),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
        })
        context['title'] = 'Словарь'
        context['url_list'] = 'ee:wordbook_list'
        context['url_word'] = 'ee:wordbook_detail'
        context['url_create_word'] = 'ee:create_wordbook'

        return context


# Text analysis
def TextAnalysis(request):

    if request.method == "POST":
        form = forms.TextAnalysisForm(request.POST)
        if form.is_valid():
            text_analysisWord(form)
        return render(request, 'text_analysis.html', {"form": form})

    else:
        form = forms.TextAnalysisForm()
    
    return render(request, "text_analysis.html", {"form": form})


# Comment
class Comment():

    def create(self, request, pk):

        if request.method == "POST" and self.is_ajax(request):
            idParent = re.findall(r'\b\d+\b', request.path)
            idWord = request.POST.get('word_id')
            newComment = models.Comment.objects.create(
                english_id=idWord,
                user_id=request.user.id,
                text=request.POST.get('text'),
                active=True,
                parent_id=idParent[0] if idWord is None else None
            )
            comment = model_to_dict(newComment)
            comment['created'] = newComment.created.strftime("%d.%m.%y")
            comment['user'] = newComment.user.username
            if newComment.user.photo:
                photo = newComment.user.photo.url
            else:
                photo = settings.DEFAULT_USER_IMAGE
            comment['image'] = photo
            response = {
                'comment': comment
            }
            return JsonResponse(response)

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


class BookListView(generic.ListView):
    template_name = 'Book/book.html'
    model = models.Book
    context_object_name = 'list'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(BookListView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Книги'
        context['url_book'] = 'ee:book_detail'
        context['inf'] = 'Нет книг'
        return context


class BookDetailView(generic.DetailView):

    template_name = 'Pages/page.html'
    model = models.Book
    context_object_name = 'detail'

    def translate(self, request):
        if request.method == "GET" and is_ajax(request):
            bookcontentObject = models.Bookcontent.objects.filter(
                id=request.GET.get('idSentence')
            ).first()

            response = {
                'translate': bookcontentObject.sentence_russian,
                'index': bookcontentObject.id,
            }
            return JsonResponse(response)

    def translateWord(self, request):
        if request.method == "GET" and is_ajax(request):
            word = request.GET.get('Word').strip().lower()
            exclude = set(string.punctuation)
            word = ''.join(ch for ch in word if ch not in exclude)
            english_object = models.English.objects.filter(
                name=word
             ).first()
            word_detail = WordDetail(english_object)

            response = {
                 'word':  word if word_detail is None else word_detail
            }
            return JsonResponse(response)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        page = self.kwargs['page']
        context.update({
            'next': models.Bookcontent.objects.all().filter(
                book=self.object,
                page__gt=page
            ).order_by('page').first(),
            'previous': models.Bookcontent.objects.all().filter(
                book=self.object,
                page__lt=page
            ).order_by('page').last(),
            'pages': models.Bookcontent.objects.values("page").distinct(
            ).order_by("page")

        })
        context['content'] = self.getContent(self.object, page)
        context['listName'] = 'Перевод'
        context['url_list'] = 'ee:verb_card_list'
        context['url_word'] = 'ee:book_detail'
        context['url_create_word'] = 'ee:verb_card_detail'
        return context

    def getContent(self, object, page):
        contentPage = []  # list массив
        content = models.Bookcontent.objects.all().filter(
            book=object,
            page=page
        )
        for item in content:
            sentences = {
                "sentence": item, "words":
                item.sentence_english.split(" ")
            }  # dict ключ-значение
            contentPage.append(sentences)

        return contentPage

    # def getWordssentence(sentence):
    #     words =[]
    #     sentence.spl
    #     for item in sentence:
    #         words.split(" ")
    #     return words


# ############################ Function handler################################
def universal(request):

    # alter_dic()
    # get_content(request)
    # import_from_excel(request)
    # export_excel(request)
    # set_sound_path()
    return render(request, 'import_success.html')


# ################################ Servis ###################################
def getComments(id):
    SetComments = models.Comment.objects.all().filter(
        english=id
    )
    listComment = []
    for item in SetComments:
        strComment = {'id': item.id,
                      'text': item.text,
                      'user': item.user,
                      'created': item.created,
                      'active': item.active,
                      'subComment': models.Comment.objects.all().filter(
                        parent_id=item.id)
                      }
        listComment.append(strComment)
    return listComment


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def WordDetail(object):

    word_detail = {
        'adjective': getJsonList(models.Adjective.objects.all().filter(
            english=object)),
        'adverb': getJsonList(models.Adverb.objects.all().filter(
            english=object)),
        'conjunction': getJsonList(models.Conjunction.objects.all().filter(
            english=object)),
        'fpos': getJsonList(models.Fpos.objects.all().filter(
            english=object)),
        'noun': getJsonList(models.Noun.objects.all().filter(
            english=object)),
        'preposition': getJsonList(models.Preposition.objects.all().filter(
            english=object)),
        'pronoun': getJsonList(models.Pronoun.objects.all().filter(
            english=object)),
        'verb': getJsonList(models.Verb.objects.all().filter(
            english=object)),
        'related': getJsonList(models.RelatedWord.objects.all().filter(
            english=object))
    }

    return word_detail


def getJsonList(queryset):

    serialized_data = serialize("json",
                                queryset,
                                use_natural_foreign_keys=True)
    serialized_data = json.loads(serialized_data)
    return serialized_data
