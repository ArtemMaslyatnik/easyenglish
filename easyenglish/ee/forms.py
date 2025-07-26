from django import forms


class UploadFileForm(forms.Form):

    title = forms.CharField(max_length=50)
    file = forms.FileField()


class TextAnalysisForm(forms.Form):

    text = forms.CharField(label='Вставьте текст', widget=forms.Textarea(
                            attrs={'class': 'form-control rounded-3'}))
    text_out = forms.CharField(required=False, label='Результат',
                               widget=forms.Textarea(
                                attrs={'class': 'form-control rounded-3'}))
    a1 = forms.CharField(required=False, max_length=50, label='Слов уровня A1',
                         widget=forms.TextInput(
                             attrs={'class': 'form-control',
                                    'readonly': 'readonly'}))
    a2 = forms.CharField(required=False, max_length=50, label='Слов уровня A2',
                         widget=forms.TextInput(
                             attrs={'class': 'form-control',
                                    'readonly': 'readonly'}))
    b1 = forms.CharField(required=False, max_length=50, label='Слов уровня B1',
                         widget=forms.TextInput(
                             attrs={'class': 'form-control',
                                    'readonly': 'readonly'}))
    other = forms.CharField(required=False, max_length=50, label='Иные слова', 
                            widget=forms.TextInput(
                             attrs={'class': 'form-control',
                                    'readonly': 'readonly'}))
    total = forms.CharField(required=False, max_length=50, label='Суммарно', 
                            widget=forms.TextInput(
                             attrs={'class': 'form-control',
                                    'readonly': 'readonly'}))