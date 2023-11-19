from django import forms

class BookRecommendForm(forms.Form):
    input = forms.Textarea()