import time
import requests
import urllib.request
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ee import models
import pandas as pd
from ee.forms import UploadFileForm
from django.db import transaction


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


# ++ parsing
def get_content(request):
    st_accept = "text/html"  # говорим веб-серверу,
    # что хотим получить html
    # имитируем подключение через браузер Mozilla на macOS
    # st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
    st_useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    # формируем хеш заголовков
    headers = {
        "Accept": st_accept,
        "User-Agent": st_useragent,
    }
    # отправляем запрос с заголовками по нужному адресу
    count = 0
    queryset = models.English.objects.all().filter(id__gt=2)
    for obj in queryset:
        count += 1
        if count > 2801:
            break
        page = "https://wooordhunt.ru/word/" + obj.name
        req = requests.get(page, headers, verify=False)
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


# updates table English after parsing
def alter_dic():
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

    return True


# set sound path data
def set_sound_path():
    for obj in models.English.objects.all():
        models.English.objects.all().filter(pk=obj.id).update(sound_path='media\\' + obj.name + '.mp3')

    return True


def import_from_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']

        df = pd.read_excel(excel_file)
        # processdfEng(df)
        processdf(df)
        processdfEngRW(df)


# ++ upload word
def processdf(df):

    for row in df.itertuples():
        id = row[1]
        tr_noun = str(row[4])
        tr_verb = str(row[5])
        tr_pronoun = str(row[6])
        tr_adjective = str(row[7])
        tr_adverb = str(row[8])
        tr_preposition = str(row[9])
        tr_conjunction = str(row[10])

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

        ngsl_number = row[1]
        engl = str(row[2])

        with transaction.atomic():
            models.English.objects.create(
                name=engl,
                ngsl_number=ngsl_number
            )


# insert data at tabla relative words
def processdfEngRW(df):

    for row in df.itertuples():
        id = row[1]
        strword = str(row[3])
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
