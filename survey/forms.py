from django import forms
from .models import Quiz, Question, Answer
from django.contrib import admin
from django.forms.models import inlineformset_factory
from django.forms.models import ModelForm, BaseInlineFormSet

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description', 'number_of_questions')



class BaseQuestionFormset(BaseInlineFormSet):

    class Meta:
        model = Question
        exclude = ()

    def add_fields(self, form, index):
        super(BaseQuestionFormset, self).add_fields(form, index)

        # save the formset in the 'nested' property
        form.nested = AnswerFormSet(
            instance=form.instance,
            data=form.data if form.is_bound else None,
            files=form.files if form.is_bound else None,
            prefix='answer-%s-%s' % (
                form.prefix,
                AnswerFormSet.get_default_prefix()),
        )

    def save(self, commit=True):

        result = super(BaseQuestionFormset, self).save(commit=commit)

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result

    def is_valid(self):
        result = super(BaseQuestionFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result

QuestionFormSet = inlineformset_factory(Quiz, Question, formset=BaseQuestionFormset, extra=1, fields=('text',))

AnswerFormSet = inlineformset_factory(Question, Answer, extra=1, fields=('text',))



