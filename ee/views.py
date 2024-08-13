import json
import re
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
    for obj in models.English.objects.all():
        count += 1
        if count > 100:
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
            tr_script_use = audio_usa.previous_sibling.previous_sibling.text
        else:
            tr_script_use = audio_usa.previous_sibling.previous_sibling.text

        audio_eng = soup.find(id="audio_uk_s")
        if audio_eng is None:
            audio_eng = soup.find(id="audio_uk")
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


def import_from_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']

        df = pd.read_excel(excel_file)
        processdf(df)
        # processdfEngRW(df)

    return render(request, 'import_success.html')


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


def processdf(df):

    for row in df.itertuples():
        id = row[1]
        # tr_verb = str(row[2])
        # tr_pronoun = str(row[2])
        # tr_adjective = str(row[2])
        # tr_adverb = str(row[3])
        tr_preposition = str(row[2])
        tr_conjunction = str(row[3])
        tr_noun = str(row[4])
        objCard = models.Card.objects.get(pk=id)
        """
        with transaction.atomic():
            if len(tr_verb) > 0 and tr_verb != 'nan':
                models.VerbCard.objects.create(english_id=objCard.id)
                arr = tr_verb.split(',')
                for item in arr:
                    item = item.strip()
                    objRus = models.Russian.objects.create(name=item.title())
                    models.Verb.objects.create(
                        card_id=objCard.id,
                        russian_id=objRus.id
                        )
         with transaction.atomic():
            if len(tr_pronoun) > 0 and tr_pronoun != 'nan':
                models.PronounCard.objects.create(english_id=objCard.id)
                arr = tr_pronoun.split(',')
                for item in arr:
                    item = item.strip()
                    objRus = models.Russian.objects.create(name=item.title())
                    models.Pronoun.objects.create(
                        card_id=objCard.id,
                        russian_id=objRus.id
                        )

            if len(tr_adjective) > 0 and tr_adjective != 'nan':
                models.AdjectiveCard.objects.create(english_id=objCard.id)
                arr = tr_adjective.split(',')
                for item in arr:
                    item = item.strip()
                    objRus = models.Russian.objects.create(name=item.title())
                    models.Adjective.objects.create(
                        card_id=objCard.id, russian_id=objRus.id)
            if len(tr_adverb) > 0 and tr_adverb != 'nan':
                models.AdverbCard.objects.create(english_id=objCard.id)
                arr = tr_adverb.split(',')
                for item in arr:
                    item = item.strip()
                    objRus = models.Russian.objects.create(name=item.title())
                    models.Adverb.objects.create(
                        card_id=objCard.id, russian_id=objRus.id)
        """
        with transaction.atomic():
            if len(tr_preposition) > 0 and tr_preposition != 'nan':
                models.PrepositionCard.objects.create(english_id=objCard.id)
                arr = tr_preposition.split(',')
                for item in arr:
                    item = item.strip()
                    objRus = models.Russian.objects.create(name=item.title())
                    models.Preposition.objects.create(
                        card_id=objCard.id,
                        russian_id=objRus.id
                    )
            if len(tr_conjunction) > 0 and tr_conjunction != 'nan':
                models.ConjunctionCard.objects.create(english_id=objCard.id)
                arr = tr_conjunction.split(',')
                for item in arr:
                    item = item.strip()
                    objRus = models.Russian.objects.create(name=item.title())
                    models.Conjunction.objects.create(
                        card_id=objCard.id,
                        russian_id=objRus.id
                    )

            if len(tr_noun) > 0 and tr_noun != 'nan':
                models.NounCard.objects.create(english_id=objCard.id)
                arr = tr_noun.split(',')
                for item in arr:
                    item = item.strip()
                    objRus = models.Russian.objects.create(name=item.title())
                    models.Noun.objects.create(card_id=objCard.id,
                                               russian_id=objRus.id)


def processdfEng(df):

    for row in df.itertuples():
        engl = str(row[2])
        ngsl_number = row[3]

        with transaction.atomic():
            objEnglish = models.English.objects.create(
                name=engl,
                ngsl_number=ngsl_number
            )
            models.Card.objects.create(english_id=objEnglish.id)


def processdfEngRW(df):

    for row in df.itertuples():
        id = row[1]
        strword = str(row[2])
        if len(strword) > 0 and strword != 'nan':
            with transaction.atomic():
                fObjCard = models.Card.objects.get(pk=id)
                arr = strword.split(',')
                for item in arr:
                    item = item.strip()
                    newObjREW = models.RelatedEnglishWord.objects.create(
                        name=item.upper()
                    )
                    models.RelatedWord.objects.create(
                        card_id=fObjCard.id,
                        relate_english_word_id=newObjREW.id
                    )


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


# Adjective
class AdjectiveCardListView(generic.ListView):
    template_name = 'Lists/list.html'
    context_object_name = 'list'
    model = models.AdjectiveCard
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(AdjectiveCardListView, self).get_context_data(**kwargs)

        context['title'] = 'Прилагательные'
        context['inf'] = 'Нет слов'
        context['url_word'] = 'ee:adjective_card_detail'
        return context


class AdjectiveCardDetailView(generic.DetailView):
    template_name = 'Items/item.html'
    model = models.AdjectiveCard
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update({
            'translate':  models.Adjective.objects.all().filter(
                card=self.object.english.id),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            'next': models.AdjectiveCard.objects.all().filter(
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.AdjectiveCard.objects.all().filter(
                english__lt=self.object.english
            ).order_by('english').last(),
        })
        context['title'] = 'Прилагательные'
        context['listName'] = 'Перевод'
        context['url_list'] = 'ee:adjective_card_list'
        context['url_word'] = 'ee:adjective_card_detail'
        context['url_create_word'] = 'ee:adjective_card_detail'

        return context


# Adverb
class AdverbCardListView(generic.ListView):
    template_name = 'Lists/list.html'
    context_object_name = 'list'
    model = models.AdverbCard
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(AdverbCardListView, self).get_context_data(**kwargs)

        context['title'] = 'Наречия'
        context['inf'] = 'Нет слов'
        context['url_word'] = 'ee:adverb_card_detail'

        return context


class AdverbCardDetailView(generic.DetailView):
    template_name = 'Items/item.html'
    model = models.AdverbCard
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update({
            'translate':  models.Adverb.objects.all().filter(
                card=self.object.english.id),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            'next': models.AdverbCard.objects.all().filter(
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.AdverbCard.objects.all().filter(
                english__lt=self.object.english
            ).order_by('english').last(),
        })
        context['title'] = 'Наречия'
        context['listName'] = 'Перевод'
        context['url_list'] = 'ee:adverb_card_list'
        context['url_word'] = 'ee:adverb_card_detail'
        context['url_create_word'] = 'ee:adverb_card_detail'

        return context


# Conjunction
class ConjunctionCardListView(generic.ListView):
    template_name = 'Lists/list.html'
    model = models.ConjunctionCard
    context_object_name = 'list'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(ConjunctionCardListView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Союзы'
        context['inf'] = 'Нет слов'
        context['url_word'] = 'ee:conjunction_card_detail'

        return context


class ConjunctionCardDetailView(generic.DetailView):
    template_name = 'Items/item.html'
    model = models.ConjunctionCard
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update({
            'translate':  models.Conjunction.objects.all().filter(
                card=self.object.english.id
            ),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            'next': models.ConjunctionCard.objects.all().filter(
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.ConjunctionCard.objects.all().filter(
                english__lt=self.object.english
            ).order_by('english').last(),
        })
        context['title'] = 'Союзы'
        context['listName'] = 'Перевод'
        context['url_list'] = 'ee:conjunction_card_list'
        context['url_word'] = 'ee:conjunction_card_detail'
        context['url_create_word'] = 'ee:conjunction_card_detail'
        return context


# Noun
class NounCardListView(generic.ListView):
    template_name = 'Lists/list.html'
    model = models.NounCard
    context_object_name = 'list'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(NounCardListView, self).get_context_data(**kwargs)

        context['title'] = 'Существительные'
        context['inf'] = 'Нет слов'
        context['url_word'] = 'ee:noun_card_detail'
        return context


class NounCardDetailView(generic.DetailView):
    template_name = 'Items/item.html'
    model = models.NounCard
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update({
            'translate':  models.Noun.objects.all().filter(
                card=self.object.english.id
            ),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            'next': models.NounCard.objects.all().filter(
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.NounCard.objects.all().filter(
                english__lt=self.object.english
            ).order_by('english').last(),
        })
        context['title'] = 'Существительные'
        context['listName'] = 'Перевод'
        context['url_word'] = 'ee:noun_card_detail'
        context['url_list'] = 'ee:noun_card_list'
        context['url_create_word'] = 'ee:noun_card_detail'
        return context


# Preposition
class PrepositionCardListView(generic.ListView):
    template_name = 'Lists/list.html'
    model = models.PrepositionCard
    context_object_name = 'list'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(PrepositionCardListView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Предлоги'
        context['inf'] = 'Нет слов'
        context['url_word'] = 'ee:preposition_card_detail'
        return context


class PrepositionCardDetailView(generic.DetailView):
    template_name = 'Items/item.html'
    model = models.PrepositionCard
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update({
            'translate':  models.Preposition.objects.all().filter(
                card=self.object.english.id
            ),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            'next': models.PrepositionCard.objects.all().filter(
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.PrepositionCard.objects.all().filter(
                english__lt=self.object.english
            ).order_by('english').last(),
        })
        context['title'] = 'Предлоги'
        context['listName'] = 'Перевод'
        context['url_list'] = 'ee:preposition_card_list'
        context['url_word'] = 'ee:preposition_card_detail'
        context['url_create_word'] = 'ee:preposition_card_detail'
        return context


# Pronoun
class PronounCardListView(generic.ListView):
    template_name = 'Lists/list.html'
    model = models.PronounCard
    context_object_name = 'list'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(PronounCardListView, self).get_context_data(**kwargs)

        context['title'] = 'Местоимения'
        context['inf'] = 'Нет слов'
        context['url_word'] = 'ee:pronoun_card_detail'
        return context


class PronounCardDetailView(generic.DetailView):
    template_name = 'Items/item.html'
    model = models.PronounCard
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update({
            'translate':  models.Pronoun.objects.all().filter(
                card=self.object.english.id
            ),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            'next': models.PronounCard.objects.all().filter(
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.PronounCard.objects.all().filter(
                english__lt=self.object.english
            ).order_by('english').last(),
        })
        context['title'] = 'Местоимения'
        context['listName'] = 'Перевод'
        context['url_list'] = 'ee:pronoun_card_list'
        context['url_word'] = 'ee:pronoun_card_detail'
        context['url_create_word'] = 'ee:pronoun_card_detail'
        return context


# Verb
class VerbCardListView(generic.ListView):
    template_name = 'Lists/list.html'
    context_object_name = 'list'
    model = models.VerbCard
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(VerbCardListView, self).get_context_data(**kwargs)

        context['title'] = 'Глаголы'
        context['inf'] = 'Нет слов'
        context['url_word'] = 'ee:verb_card_detail'
        return context


class VerbCardDetailView(generic.DetailView):
    template_name = 'Items/item.html'
    model = models.VerbCard
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context.update({
            'translate': models.Verb.objects.all().filter(
                card=self.object.english.id
            ),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            'next': models.VerbCard.objects.all().filter(
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.VerbCard.objects.all().filter(
                english__lt=self.object.english
            ).order_by('english').last(),
        })
        context['title'] = 'Глаголы'
        context['listName'] = 'Перевод'
        context['url_list'] = 'ee:verb_card_list'
        context['url_word'] = 'ee:verb_card_detail'
        context['url_create_word'] = 'ee:verb_card_detail'
        return context


# Card
class CardListView(generic.ListView):
    template_name = 'Lists/list.html'
    model = models.Card
    context_object_name = 'list'
    paginate_by = 10

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(CardListView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Слова по релевантности'
        context['url_word'] = 'ee:card_detail'
        context['inf'] = 'Нет слов'
        return context


class CardDetailView(generic.DetailView):
    template_name = 'Card/card_detail.html'
    model = models.Card
    context_object_name = 'detail'
    textSQlComment = ('SELECT '
                      '1 as id, '
                      't1.text AS text1, '
                      't1.created AS created1, '
                      't1.active AS active1, '
                      't1.english_id AS english1, '
                      'au1.username AS user1, '
                      't2.text AS text2, '
                      't2.created AS created2, '
                      't2.active AS active2, '
                      'au2.username AS user2 '
                      'FROM '
                      'ee_comment AS t1 '
                      'LEFT JOIN ee_comment AS t2 ON t2.parent_id = t1.id '
                      'LEFT JOIN auth_user AS au1 ON au1.id = t1.user_id '
                      'LEFT JOIN auth_user AS au2 ON au2.id = t2.user_id '
                      'WHERE t1.english_id = 1 '
                      )

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context.update({
            'adjective_list': models.Adjective.objects.all().filter(
                card=self.object
            ),
            'adverb_list': models.Adverb.objects.all().filter(
                card=self.object
            ),
            'conjunction_list': models.Conjunction.objects.all().filter(
                card=self.object
            ),
            'fpos_list': models.Fpos.objects.all().filter(
                card=self.object
            ),
            'noun_list': models.Noun.objects.all().filter(
                card=self.object
            ),
            'preposition_list': models.Preposition.objects.all().filter(
                card=self.object
            ),
            'pronoun_list': models.Pronoun.objects.all().filter(
                card=self.object
            ),
            'related_list': models.RelatedWord.objects.all().filter(
                card=self.object
            ),
            'verb_list': models.Verb.objects.all().filter(
                card=self.object
            ),
            'wordbook': models.Wordbook.objects.all().filter(
                english=self.object.english,
                user_id=self.request.user.id
            ),
            # 'comments': models.Comment.objects.raw(self.textSQlComment),
            'comments': self.getComments(),
            'next': models.Card.objects.all().filter(
                english__gt=self.object.english
            ).order_by('english').first(),
            'previous': models.Card.objects.all().filter(
                english__lt=self.object.english
            ).order_by('english').last(),
        })
        context['title'] = 'Слова по релевантности'
        context['url_list'] = 'ee:card_list'
        context['url_word'] = 'ee:card_detail'
        context['url_create_word'] = 'ee:card_detail'
        return context

    def getComments(self):
        SetComments = models.Comment.objects.all().filter(
            english_id=self.object.id
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


# Wordbook
class WordbookListView(LoginRequiredMixin, generic.ListView):

    template_name = 'Lists/list.html'
    model = models.Wordbook
    context_object_name = 'list'
    paginate_by = 10

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        return qs.filter(user_id=self.request.user.id)

    def create(self, request, pk):

        if request.method == "POST" and self.is_ajax(request):
            if request.path == request.POST.get('path'):
                querySet = models.Wordbook.objects.filter(
                    id=pk,
                    user_id=request.user.id
                )
            else:
                querySet = models.Wordbook.objects.filter(
                    english_id=pk,
                    user_id=request.user.id
                )
            if querySet.count() > 0:
                querySet.delete()
                response = {
                    'wordbook_list': False
                }
            else:
                models.Wordbook.objects.create(
                    english_id=pk,
                    user_id=request.user.id
                )
                response = {
                    'wordbook_list': True
                }
        return JsonResponse(response)

    def is_ajax(self, request):
        return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        context = super(WordbookListView,
                        self).get_context_data(**kwargs)

        context['title'] = 'Словарик'
        context['url_word'] = 'ee:wordbook_detail'
        context['inf'] = 'Нет слов'
        return context


class WordbookDetailView(LoginRequiredMixin, generic.DetailView):

    template_name = 'Card/card_detail.html'
    model = models.Wordbook
    context_object_name = 'detail'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet
        context.update({
            'adjective_list': models.Adjective.objects.all().filter(
                card=self.object.english_id
            ),
            'adverb_list': models.Adverb.objects.all().filter(
                card=self.object.english_id
            ),
            'conjunction_list': models.Conjunction.objects.all().filter(
                card=self.object.english_id
            ),
            'fpos_list': models.Fpos.objects.all().filter(
                card=self.object.english_id
            ),
            'noun_list': models.Noun.objects.all().filter(
                card=self.object.english_id
            ),
            'preposition_list': models.Preposition.objects.all().filter(
                card=self.object.english_id
            ),
            'pronoun_list': models.Pronoun.objects.all().filter(
                card=self.object.english_id
            ),
            'related_list': models.RelatedWord.objects.all().filter(
                card=self.object.english_id
            ),
            'verb_list': models.Verb.objects.all().filter(
                card=self.object.english_id
            ),
            'wordbook_list': models.Wordbook.objects.all().filter(
                english=self.object.english_id,
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
            englishObject = models.English.objects.filter(
                name=word
             ).first()
            cardDetail = CardDetail(englishObject)

            response = {
                 'word':  word if cardDetail is None else cardDetail
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


# ################################ Servis ###################################
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


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def CardDetail(object):

    CardDetail = {
        'adjective': getJsonList(models.Adjective.objects.all().filter(
            card_id=object.id
        )),
        'adverb': getJsonList(models.Adverb.objects.all().filter(
            card_id=object.id
        )),
        'conjunction': getJsonList(models.Conjunction.objects.all().filter(
            card_id=object.id
        )),
        'fpos': getJsonList(models.Fpos.objects.all().filter(
            card_id=object.id
        )),
        'noun': getJsonList(models.Noun.objects.all().filter(
            card_id=object.id
        )),
        'preposition': getJsonList(models.Preposition.objects.all().filter(
            card_id=object.id
        )),
        'pronoun': getJsonList(models.Pronoun.objects.all().filter(
            card_id=object.id
        )),
        'verb': getJsonList(models.Verb.objects.all().filter(
            card_id=object.id
        )),
        'related': getJsonList(models.RelatedWord.objects.all().filter(
                card_id=object.id
        ))
    }

    return CardDetail


def getJsonList(queryset):

    serialized_data = serialize("json", queryset, use_natural_foreign_keys=True)
    serialized_data = json.loads(serialized_data)
    return serialized_data
