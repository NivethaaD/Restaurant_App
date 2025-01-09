# forms.py

from django import forms
from .models import UserReview

class UserReviewForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['rating', 'review_text']

class UserReviewEditForm(forms.ModelForm):
    class Meta:
        model = UserReview
        fields = ['rating', 'review_text']
