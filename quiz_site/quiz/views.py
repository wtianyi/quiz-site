from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import Quiz, Question, Choice


# Create your views here.

# All quizzes
def index(request):
    all_quiz_list = Quiz.objects.all()
    context = {
        'all_quiz_list': all_quiz_list,
    }

    return render(request, 'quiz/index.html', context)


# Specific quiz
def single_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)

    return render(request, 'quiz/single_quiz.html', {'quiz': quiz})


# Specific question
def single_question(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    current_question = quiz.question_set.get(pk=question_id)

    # Checks if currently on last question of quiz
    last_question_check = False
    if question_id == (len(quiz.question_set.all())):
        last_question_check = True

    next_question_id = question_id+1

    all_choices = current_question.choice_set.all()

    context = {
        'current_question': current_question,
        'all_choices': all_choices,
        'quiz': quiz,
        'next_question_id': next_question_id,
        'last_question_check': last_question_check
    }

    return render(request, 'quiz/single_question.html', context)


def vote(request, quiz_id, question_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    current_question = quiz.question_set.get(pk=question_id)
    try:
        selected_choice = current_question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'quiz/single_question.html', {
            'quiz': quiz,
            'current_question': current_question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # selected_choice.votes += 1
        # selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.    last_question_check = False
        if question_id == (len(quiz.question_set.all())):
            return HttpResponseRedirect(reverse('quiz:results', args=(quiz.id,)))
        else :
            return HttpResponseRedirect(reverse('quiz:single_question', args=(quiz.id, question_id+1,)))



# Quiz results
def results(request, quiz_id):
    return render(request, 'quiz/results.html')