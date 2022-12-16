from django import forms
from .models import Quiz, Question, Answer
from django.contrib import admin
from django.forms.models import inlineformset_factory
from django.forms.models import ModelForm, BaseInlineFormSet


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ('title', 'description')


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
        print("TRY TO SAVE")

        for form in self.forms:
            if hasattr(form, 'nested'):
                if not self._should_delete_form(form):
                    form.nested.save(commit=commit)

        return result


    def save_new(self, form, commit=True):
        """Saves and returns a new model instance for the given form."""

        print("TRY TO SAVE NEW")
        instance = super(BaseQuestionFormset, self).save_new(form, commit=commit)


        # update the form’s instance reference
        form.instance = instance

        # update the instance reference on nested forms
        for nested in form.nested:
            nested.instance = instance

            # iterate over the cleaned_data of the nested formset and update the foreignkey reference
            for cd in nested.cleaned_data:
                cd[nested.fk] = instance

        return instance

    def save_all(self, commit=True):
        """Save all formsets and along with their nested formsets."""

        # Save without committing (so self.saved_forms is populated)
        # — We need self.saved_forms so we can go back and access
        #    the nested formsets
        print("TRY TO SAVE ALL")
        objects = self.save(commit=False)

        # Save each instance if commit=True
        if commit:
            for o in objects:
                o.save()

        # save many to many fields if needed
        #if not commit:
        #    self.save_m2m()

        # save the nested formsets
        for form in set(self.initial_forms + self.saved_forms):
            if self.should_delete(form): continue

            for nested in form.nested:
                nested.save(commit=commit)


    def is_valid(self):
        result = super(BaseQuestionFormset, self).is_valid()

        if self.is_bound:
            for form in self.forms:
                if hasattr(form, 'nested'):
                    result = result and form.nested.is_valid()

        return result


QuestionFormSet = inlineformset_factory(Quiz,
                                        Question,
                                        formset=BaseQuestionFormset,
                                        labels={'text': 'question', 'type': 'question_type'},
                                        extra=0,
                                        min_num=2,
                                        max_num=10,
                                        fields='__all__',
                                        widgets={
                                            'text': forms.TextInput(
                                                attrs={
                                                    'class': 'form-control',
                                                    'placeholder': 'Question',
                                                }
                                            )
                                    })

AnswerFormSet = inlineformset_factory(Question,
                                      Answer,
                                      labels={'text': 'answer'},
                                      extra=0,
                                      min_num=2,
                                      fields='__all__',
                                      widgets={
                                        'text': forms.TextInput(
                                            attrs={
                                                'class': 'form-control',
                                                'placeholder': 'Answer',
                                            }
                                        )
                                    })



