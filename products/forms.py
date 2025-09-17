# products/forms.py
from django import forms

class ReviewForm(forms.Form):
    review_text = forms.CharField(widget=forms.Textarea, label='Review')
    rating = forms.IntegerField(min_value=1, max_value=5, label='Rating')
