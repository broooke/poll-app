from django import forms
from .models import Question, Choice

class voteForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('question_text',)

class voteForm1(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text','question')


