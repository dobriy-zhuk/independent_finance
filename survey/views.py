from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Quiz, Question, Answer, Marks_Of_User
from django.http import JsonResponse
from django.forms import inlineformset_factory



#@login_required(login_url = 'l')
def testing(request):
    if request.method == 'POST':
        questions = Question.objects.all()
        score = 0
        wrong = 0
        correct = 0
        total = 0
        for q in questions:
            total += 1
            print(request.POST.get(q.content))
            print(q.ans)
            print()
            if q.ans == request.POST.get(q.content):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score / (total * 10) * 100
        context = {
            'score': score,
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total
        }
        return render(request, 'survay/results.html', context)
    else:
        quizes = Quiz.objects.all()
        context = {
            'quizs': quizes
        }
        return render(request, 'survay/testing.html', context)

"""
def add_quiz(request):
    if request.user.is_staff:
        form = QuizForm()

        if (request.method == 'POST'):
            form = QuizForm(request.POST)
            if (form.is_valid()):
                quiz_form = form.save()
                return HttpResponseRedirect(reverse(add_question, args=(quiz_form.pk,)))
        context = {'form': form}
        return render(request, 'survay/add_quiz.html', context)
    else:

        return redirect('settings')



def add_question(request):
    questions = Question.objects.all()
    questions = Question.objects.filter().order_by('-id')
    if request.method=="POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "survay/add_question.html")
    else:
        form=QuestionForm()
    return render(request, "survay/add_question.html", {'form':form, 'questions':questions})

def delete_question(request, myid):
    question = Question.objects.get(id=myid)
    if request.method == "POST":
        question.delete()
        return redirect('/add_question')
    return render(request, "survay/delete_question.html", {'question':question})


def add_options(request, myid):
    question = Question.objects.get(id=myid)
    QuestionFormSet = inlineformset_factory(Question, Answer, fields=('content','correct', 'question'), extra=4)
    if request.method=="POST":
        formset = QuestionFormSet(request.POST, instance=question)
        if formset.is_valid():
            formset.save()
            alert = True
            return render(request, "survay/add_options.html", {'alert':alert})
    else:
        formset=QuestionFormSet(instance=question)
    return render(request, "survay/add_options.html", {'formset':formset, 'question':question})


def results(request):
    marks = Marks_Of_User.objects.all()
    return render(request, "survay/results.html", {'marks':marks})


def delete_result(request, myid):
    marks = Marks_Of_User.objects.get(id=myid)
    if request.method == "POST":
        marks.delete()
        return redirect('/results')
    return render(request, "survay/delete_result.html", {'marks':marks})
"""