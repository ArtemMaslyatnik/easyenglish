import json
import re
import string
import time
import requests
import urllib.request
from bs4 import BeautifulSoup
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from ee import models
from django.views import generic
import pandas as pd
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin
from ee.forms import UploadFileForm
from django.core.serializers import serialize


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

    def getComments(self):
        SetComments = models.Comment.objects.all().filter(
            english=self.object
        )
        listComment = []
        for item in SetComments:
            strComment = {'id': item.id,
                          'text': item.text,
                          'user': item.user,
                          'created': item.created,
                          'active': item.active,
                          'subComment': models.Comment.objects.all().filter(
                              parent_id=item.id
                          )
                          }
            listComment.append(strComment)
        return listComment

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
            'comments': self.getComments(),
            'next': models.English.objects.all().filter(
                id__gt=self.object.id
            ).order_by('id').first(),
            'previous': models.English.objects.all().filter(
                id__lt=self.object.id
            ).order_by('id').last(),
        })
        context['title'] = 'Слова по релевантности'
        context['url_list'] = 'ee:english_words'
        context['url_word'] = 'ee:word_detail'
        context['url_create_word'] = 'ee:create_wordbook'
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


# Comment
class Comment():

    def create(self, request, pk):

        if request.method == "POST" and self.is_ajax(request):
            idCard = re.findall(r'\b\d+\b', request.path)
            idParent = request.POST.get('parent-comment')
            newComment = models.Comment.objects.create(
                english_id=idCard[0] if idParent == idCard else None,
                user_id=request.user.id,
                text=request.POST.get('text'),
                active=True,
                parent_id=None if idParent == idCard else idParent
            )
            comment = model_to_dict(newComment)
            comment['created'] = newComment.created.strftime("%d.%m.%y")
            comment['user'] = newComment.user.username
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
    for obj in models.English.objects.all():
        if obj.sound_path.name.find('audio') >= 0:
            sound_path = obj.sound_path.name
            new_sound_path = sound_path.replace('audio', 'media')
            models.English.objects.all().filter(pk=obj.id).update(sound_path=new_sound_path)

    return render(request, 'import_success.html')


# ++ parsing
def get_content(request):
    st_accept = "text/html"  # говорим веб-серверу,
    # что хотим получить html
    # имитируем подключение через браузер Mozilla на macOS
    st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    # формируем хеш заголовков
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent
    }
    # отправляем запрос с заголовками по нужному адресу
    count = 0
    queryset = models.English.objects.all().filter(id__gt=2701)
    for obj in queryset:
        count += 1
        if count > 1:
            break
        page = "https://wooordhunt.ru/word/" + obj.name
        req = requests.get(page, headers)
        time.sleep(10)
        # считываем текст HTML-документа
        src = req.text
        # print(src)
        # инициализируем html-код страницы
        soup = BeautifulSoup(src, 'lxml')
        # считываем заголовок страницы
        # title = soup.title.string

        # english_word
        english_word = soup.find(id="wd_title")
        english_word = english_word.h1.text

        # tr_script
        audio_usa = soup.find(id="audio_us_s")
        if audio_usa is None:
            audio_usa = soup.find(id="audio_us")
            if audio_usa is None:
                audio_usa = soup.find(id="audio_us_1")
                tr_script_use = audio_usa.previous_sibling.previous_sibling.text
            else:
                tr_script_use = audio_usa.previous_sibling.previous_sibling.text
        else:
            tr_script_use = audio_usa.previous_sibling.previous_sibling.text

        audio_eng = soup.find(id="audio_uk_s")
        if audio_eng is None:
            audio_eng = soup.find(id="audio_uk")
            if audio_eng is None:
                audio_eng = soup.find(id="audio_uk_1")
                try:
                    tr_script_eng = audio_eng.previous_sibling.previous_sibling.text
                except Exception:
                    tr_script_eng = 'NO'
            else:
                tr_script_eng = audio_eng.previous_sibling.previous_sibling.text
        else:
            tr_script_eng = audio_eng.previous_sibling.previous_sibling.text

        # audio
        url = audio_eng.source.attrs['src']
        destination = 'audio/' + english_word + '.mp3'
        full_url = 'https://wooordhunt.ru/' + url
        urllib.request.urlretrieve(full_url, destination)

        content_russian = soup.find(id="content_in_russian")
        for child in content_russian.children:
            count_noun = 0
            count_verb = 0
            count_adjective = 0
            count_adverb = 0
            count_conjunction = 0
            count_preposition = 0
            count_pronoun = 0
            if hasattr(child, "text"):
                if child.name == 'div' and 'class' in child.attrs:
                    if child.attrs['class'][0] == 't_inline_en':
                        basic_meaning = child.text
                elif child.name == 'h4' and 'class' in child.attrs:
                    # noun
                    if (child.attrs['class'][0] == 'pos_item' and child.text.find('существительное') >= 0):
                        # finde all tag
                        spans = child.next_sibling.find_all('span')
                        for span in spans:
                            if not span.attrs.get('class', None):
                                onclick = span.attrs.get('onclick', None)
                                if onclick.find('showMoreEx') >= 0:
                                    continue
                                if count_noun > 4:
                                    break
                                text = span.text
                                models.Serv.objects.create(
                                    english=english_word,
                                    parts_speech='noun',
                                    translate=text,
                                    transcription_eng=tr_script_eng,
                                    transcription_use=tr_script_use,
                                    sound_path=destination
                                )
                                count_noun += 1
                    # verb
                    elif (child.attrs['class'][0] == 'pos_item' and child.text.find('глагол') >= 0):
                        # finde all tag
                        spans = child.next_sibling.find_all('span')
                        for span in spans:
                            if not span.attrs.get('class', None):
                                onclick = span.attrs.get('onclick', None)
                                if onclick.find('showMoreEx') >= 0:
                                    continue
                                if count_verb > 4:
                                    break
                                text = span.text
                                models.Serv.objects.create(
                                    english=english_word,
                                    parts_speech='verb',
                                    translate=text,
                                    transcription_eng=tr_script_eng,
                                    transcription_use=tr_script_use,
                                    sound_path=destination
                                )
                                count_verb += 1
                    # adjective
                    elif (child.attrs['class'][0] == 'pos_item' and child.text.find('прилагательное') >= 0):
                        # finde all tag
                        spans = child.next_sibling.find_all('span')
                        for span in spans:
                            if not span.attrs.get('class', None):
                                onclick = span.attrs.get('onclick', None)
                                if onclick.find('showMoreEx') >= 0:
                                    continue
                                if count_adjective > 4:
                                    break
                                text = span.text
                                models.Serv.objects.create(
                                    english=english_word,
                                    parts_speech='adjective',
                                    translate=text,
                                    transcription_eng=tr_script_eng,
                                    transcription_use=tr_script_use,
                                    sound_path=destination
                                )
                                count_adjective += 1
                    # adverb
                    elif (child.attrs['class'][0] == 'pos_item' and child.text.find('наречие') >= 0):
                        # finde all tag
                        spans = child.next_sibling.find_all('span')
                        for span in spans:
                            if not span.attrs.get('class', None):
                                onclick = span.attrs.get('onclick', None)
                                if onclick.find('showMoreEx') >= 0:
                                    continue
                                if count_adverb > 4:
                                    break
                                text = span.text
                                models.Serv.objects.create(
                                    english=english_word,
                                    parts_speech='adverb',
                                    translate=text,
                                    transcription_eng=tr_script_eng,
                                    transcription_use=tr_script_use,
                                    sound_path=destination
                                )
                                count_adverb += 1
                    # conjunction
                    elif (child.attrs['class'][0] == 'pos_item' and child.text.find('союз') >= 0):
                        # finde all tag
                        spans = child.next_sibling.find_all('span')
                        for span in spans:
                            if not span.attrs.get('class', None):
                                onclick = span.attrs.get('onclick', None)
                                if onclick.find('showMoreEx') >= 0:
                                    continue
                                if count_conjunction > 4:
                                    break
                                text = span.text
                                models.Serv.objects.create(
                                    english=english_word,
                                    parts_speech='conjunction',
                                    translate=text,
                                    transcription_eng=tr_script_eng,
                                    transcription_use=tr_script_use,
                                    sound_path=destination
                                )
                                count_conjunction += 1
                    # preposition
                    elif (child.attrs['class'][0] == 'pos_item' and child.text.find('предлог') >= 0):
                        # finde all tag
                        spans = child.next_sibling.find_all('span')
                        for span in spans:
                            if not span.attrs.get('class', None):
                                onclick = span.attrs.get('onclick', None)
                                if onclick.find('showMoreEx') >= 0:
                                    continue
                                if count_preposition > 4:
                                    break
                                text = span.text
                                models.Serv.objects.create(
                                    english=english_word,
                                    parts_speech='preposition',
                                    translate=text,
                                    transcription_eng=tr_script_eng,
                                    transcription_use=tr_script_use,
                                    sound_path=destination
                                )
                                count_preposition += 1
                    # pronoun
                    elif (child.attrs['class'][0] == 'pos_item' and child.text.find('местоимение') >= 0):
                        # finde all tag
                        spans = child.next_sibling.find_all('span')
                        for span in spans:
                            if not span.attrs.get('class', None):
                                onclick = span.attrs.get('onclick', None)
                                if onclick.find('showMoreEx') >= 0:
                                    continue
                                if count_pronoun > 4:
                                    break
                                text = span.text
                                models.Serv.objects.create(
                                    english=english_word,
                                    parts_speech='pronoun',
                                    translate=text,
                                    transcription_eng=tr_script_eng,
                                    transcription_use=tr_script_use,
                                    sound_path=destination
                                )
                                count_pronoun += 1
    return render(request, 'import_success.html')


# updates table English after parsing
def alter_dic(request):
    query_text = (' SELECT 1 as id, serv.english, dic.name,  serv.transcription_use, serv.sound_path, serv.sound_path'
                  ' FROM ee_serv AS serv'
                  '     RIGHT JOIN ee_english AS dic'
                  '     ON lower(serv.english)  = dic.name'
                  ' GROUP BY  serv.english,dic.name, serv.transcription_use, serv.sound_path'
                  ' ORDER BY "english"')

    for obj in models.English.objects.raw(query_text):
        find_obj = models.English.objects.all().filter(name=obj.name)
        transcription = "" if obj.transcription_use is None else obj.transcription_use
        sound_path = "" if obj.sound_path is None else obj.sound_path
        find_obj.update(transcription=transcription, sound_path=sound_path)

    return render(request, 'import_success.html')


# fix content
def export_excel(request):
    # create DataFrame
    query_text = ('SELECT serv.english, dic.name,  dic.id'
                  ' FROM ee_serv AS serv'
                  '     RIGHT JOIN ee_english AS dic'
                  '     ON lower(serv.english)  = dic.name'
                  ' WHERE serv.english IS NULL'
                  ' GROUP BY serv.english, dic.name, dic.id'
                  ' ORDER BY "english" desc'
                  ' LIMIT 100')

    english_list = []
    name_list = []
    id_list = []
    for obj in models.English.objects.raw(query_text):
        english_list.append(obj.english)
        name_list.append(obj.name)
        id_list.append(obj.id)
    dic = {'english': english_list, 'name': name_list, 'id': id_list}
    df = pd.DataFrame(dic)
    df.to_excel(r'C:\Users\lykov\Documents\mydata.xlsx')

    return render(request, 'import_success.html')
# -- parsing


def import_from_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']

        df = pd.read_excel(excel_file)
        processdf(df)
        # processdfEngRW(df)

    return render(request, 'import_success.html')


# Book content
def upload_file(request):

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # handle_uploaded_file(request.FILES["file"])
            handle_duble_uploaded_file(
                request.FILES["file"],
                request.FILES["file-rus"]
            )
            return HttpResponseRedirect("/index")
    else:
        form = UploadFileForm()
    return render(request, "index.html", {"form": form})


# ################################ Servis ###################################
# ++ Book content
def handle_uploaded_file(f):
    numberPage = 0
    for chunk in f.chunks():
        sentences = chunk.decode().split(".")
        for item in sentences:
            stringSearch = item.upper()
            if stringSearch.find('CHAPTER') > 0:
                numberPage += 1
            models.Bookcontent.objects.create(
                sentence_english=item + '.',
                sentence_russian="",
                page=numberPage,
                book=None
            )
    # if request.method == 'POST':
    #     form = UploadFileForm(request.POST, request.FILES)
    #     file = request.FILES['rtf_file']
    #     # filepauth = "C:\\Users\\lykov\\Downloads\\Peter_Pan-J_M_Barrie.txt"
    #     numberPage = 0
    #     # with open(rtf_file, "r") as file:
    #     text = file.read()
    #     # for line in file:
    #     # print(text, end="")
    #     sentences = text.split(".")
    #     for item in sentences:
    #         stringSearch = item.upper()
    #         if stringSearch.find('CHAPTER') > 0:
    #             numberPage += 1
    #         models.Bookcontent.objects.create(
    #             sentence_english=item + '.',
    #             sentence_russian="",
    #             page=numberPage,
    #             book=1
    #         )
    # return render(request, 'import_success.html')


def handle_duble_uploaded_file(fEng, fRus):

    Book = models.Book.objects.create(
        title="Peter Pan",
        level=None,
        unique_words=543,
        total_words=3182,
        description='Питер Пэн является одним из самых популярных персонажей'
        + 'детской литературы ХХ века. Это простая и волшебная история о сказочном'
        + 'мальчике, который не хотел взрослеть. Питер сбежал из дома и стал вечно'
        + 'молодым. Он жил в компании маленьких мальчиков, которые потеряли в лесу.'
        + 'Однажды Питер Пэн влетел в детскую, где девочка Венди и двое ее младших'
        + 'братьев, и он изменил жизнь этих детей навсегда. Они ехали с Питера на'
        + 'Дальний остров чудо под названием Неверлэнд. Там они встретились с'
        + 'русалки, храбрые индейцы, озорная Фея и даже пираты с их злобным'
        + 'мастером капитан крюк. Судьба капитана крюка будет зависеть от рук'
        + 'Питера Пэна, его главный враг. Захватывающие, романтические и'
        + 'опасные приключения ждут героев.'
    )
    numberPage = 0
    sentencesEngList = fEng.read().decode().split(".")
    sentencesRusList = fRus.read().decode().split(".")

    for i, sentence in enumerate(sentencesEngList):
        sentenceClin = sentence.translate(
            str.maketrans({'\n': '', '\t': '', '\r': ''}))
        sentenceClinRus = sentencesRusList[i].translate(
            str.maketrans({'\n': '', '\t': '', '\r': ''}))
        stringSearch = sentenceClin.upper()
        stringSearchRus = sentenceClinRus.upper()
        # title page
        chapterNnmber = stringSearch.find('CHAPTER')
        chapterNnmberRus = stringSearchRus.find('ГЛАВА')
        if chapterNnmber > -1:
            titleEng = []
            titleRus = []
            numberPage += 1
            signNumber = stringSearch.find('!')
            # signNumberRus = sentenceClinRus.find('!')
            # mark '!' at the end of the line
            if chapterNnmber > signNumber and signNumber != -1:

                endSentence = sentenceClin[:chapterNnmber]
                endSentenceRus = sentenceClinRus[:chapterNnmberRus]
                models.Bookcontent.objects.create(
                    sentence_english=endSentence,
                    sentence_russian=endSentenceRus,
                    page=numberPage-1,
                    book=Book
                )

                titleSentenceEng = sentenceClin[chapterNnmber:].split(" ")
                titleSentenceRus = sentenceClinRus[chapterNnmberRus:].split(
                    " ")

                # eng
                titleEng.append(
                    titleSentenceEng[0] + " " + titleSentenceEng[1])
                quantity = len(titleSentenceEng[0])+len(titleSentenceEng[1])+2
                titleEng.append(sentenceClin[chapterNnmber+quantity:])

                # rus
                titleRus.append(
                    titleSentenceRus[0] + " " + titleSentenceRus[1])
                quantity = len(titleSentenceRus[0])+len(titleSentenceRus[1])+2
                titleRus.append(sentenceClinRus[chapterNnmberRus+quantity:])

                for y, titlePage in enumerate(titleEng):
                    chapter = (y == 0) or False
                    models.Bookcontent.objects.create(
                        sentence_english=titlePage,
                        sentence_russian=titleRus[y],
                        page=numberPage,
                        book=Book,
                        chapter=chapter,
                        chapterName=not chapter
                    )

            else:
                titleSentenceEng = sentenceClin.split(" ")
                titleSentenceRus = sentenceClinRus.split(" ")

                # eng
                titleEng.append(
                    titleSentenceEng[0] + " " + titleSentenceEng[1])
                quantity = len(titleSentenceEng[0])+len(titleSentenceEng[1])+2
                titleEng.append(sentenceClin[quantity:])

                # rus
                titleRus.append(
                    titleSentenceRus[0] + " " + titleSentenceRus[1])
                quantity = len(titleSentenceRus[0])+len(titleSentenceRus[1])+2
                titleRus.append(sentenceClinRus[quantity:])

                for y, titlePage in enumerate(titleEng):
                    chapter = (y == 0) or False
                    models.Bookcontent.objects.create(
                        sentence_english=titlePage,
                        sentence_russian=titleRus[y],
                        page=numberPage,
                        book=Book,
                        chapter=chapter,
                        chapterName=not chapter
                    )
        else:
            models.Bookcontent.objects.create(
                sentence_english=sentence + '.',
                sentence_russian=sentencesRusList[i] + '.',
                page=numberPage,
                book=Book
            )
# -- Book content


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


# ++ upload word
def processdf(df):

    for row in df.itertuples():
        id = row[1]
        tr_noun = str(row[2])
        tr_verb = str(row[3])
        tr_pronoun = str(row[4])
        tr_adjective = str(row[5])
        tr_adverb = str(row[6])
        tr_preposition = str(row[7])
        tr_conjunction = str(row[8])

        obj_english = models.English.objects.get(pk=id)

        with transaction.atomic():
            if len(tr_noun) > 0 and tr_noun != 'nan':
                arr = tr_noun.split(',')
                for item in arr:
                    item = item.strip()
                    obj_rus = models.Russian.objects.create(name=item.capitalize())
                    models.Noun.objects.create(
                        english=obj_english,
                        russian=obj_rus)
            if len(tr_verb) > 0 and tr_verb != 'nan':
                arr = tr_verb.split(',')
                for item in arr:
                    item = item.strip()
                    obj_rus = models.Russian.objects.create(name=item.capitalize())
                    models.Verb.objects.create(
                        english=obj_english,
                        russian=obj_rus)
            if len(tr_pronoun) > 0 and tr_pronoun != 'nan':
                arr = tr_pronoun.split(',')
                for item in arr:
                    item = item.strip()
                    obj_rus = models.Russian.objects.create(name=item.capitalize())
                    models.Pronoun.objects.create(
                        english=obj_english,
                        russian=obj_rus)
            if len(tr_adjective) > 0 and tr_adjective != 'nan':
                arr = tr_adjective.split(',')
                for item in arr:
                    item = item.strip()
                    obj_rus = models.Russian.objects.create(name=item.capitalize())
                    models.Adjective.objects.create(
                        english=obj_english,
                        russian=obj_rus)
            if len(tr_adverb) > 0 and tr_adverb != 'nan':
                arr = tr_adverb.split(',')
                for item in arr:
                    item = item.strip()
                    obj_rus = models.Russian.objects.create(name=item.capitalize())
                    models.Adverb.objects.create(
                        english=obj_english,
                        russian=obj_rus)
            if len(tr_preposition) > 0 and tr_preposition != 'nan':
                arr = tr_preposition.split(',')
                for item in arr:
                    item = item.strip()
                    obj_rus = models.Russian.objects.create(name=item.capitalize())
                    models.Preposition.objects.create(
                        english=obj_english,
                        russian=obj_rus)
            if len(tr_conjunction) > 0 and tr_conjunction != 'nan':
                arr = tr_conjunction.split(',')
                for item in arr:
                    item = item.strip()
                    obj_rus = models.Russian.objects.create(name=item.capitalize())
                    models.Conjunction.objects.create(
                        english=obj_english,
                        russian=obj_rus)


# insert data at tabla english
def processdfEng(df):

    for row in df.itertuples():
        engl = str(row[2])
        ngsl_number = row[3]

        with transaction.atomic():
            models.English.objects.create(
                name=engl,
                ngsl_number=ngsl_number
            )


# insert data at tabla relative words
def processdfEngRW(df):

    for row in df.itertuples():
        id = row[1]
        strword = str(row[2])
        if len(strword) > 0 and strword != 'nan':
            with transaction.atomic():
                fObjEnglish = models.English.objects.get(pk=id)
                arr = strword.split(',')
                for item in arr:
                    item = item.strip()
                    newObjREW = models.RelatedEnglishWord.objects.create(
                        name=item.title()
                    )
                    models.RelatedWord.objects.create(
                        english_id=fObjEnglish.id,
                        relate_english_word_id=newObjREW.id
                    )
# -- upload word
