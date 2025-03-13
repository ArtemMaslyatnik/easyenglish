from ee import models
from django.db import transaction

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