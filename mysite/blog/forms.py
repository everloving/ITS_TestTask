from django import forms

class QueryForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Enter your text', max_length=50)


