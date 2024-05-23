import json
import random
from datetime import timedelta
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.db.models import Sum, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from .forms import LoginForm, SignUpForm
from .models import UserProfile, Test, Questions, Result, ActiveTest
from .utils import get_token


@csrf_protect
def admin_settings_view(request):
    return render(request, 'home.html')


@csrf_protect
def tests(request):
    test = Test.objects.filter(user=request.user)
    return render(request, 'tests/index.html', {'tests': test})


@csrf_protect
def test_get(request, id):
    test = get_object_or_404(Test, id=id, user=request.user)
    return render(request, 'tests/get.html', {'test': test})


@csrf_protect
def start_test(request, id):
    try:
        test = get_object_or_404(Test, id=id, user=request.user)
        f = request.GET.get('f')
        l = request.GET.get('l')
        if f and l:
            try:
                f = int(f)
                l = int(l)
                questions = Questions.objects.filter(test=test, id__gte=f, id__lte=l)
            except ValueError:
                questions = Questions.objects.filter(test=test)
        else:
            questions = Questions.objects.filter(test=test)

        questions_list = list(questions)
        random.shuffle(questions_list)
        active_test_data = []
        for question in questions_list:
            variants = json.loads(question.variants)
            random.shuffle(variants)
            active_test_data.append({
                "question": question.question,
                "variants": variants,
                "answer": json.loads(question.answer),
                "your_answer": '',
            })
        active_test = ActiveTest.objects.create(
            user=request.user,
            variants=json.dumps(active_test_data)
        )
        return redirect(reverse('testing', args=[active_test.id]) + f'?question=1')
    except:
        return redirect(reverse('tests'))


@csrf_protect
def testing(request, id):
    try:
        active_test = get_object_or_404(ActiveTest, id=id, user=request.user)
        question_param = request.GET.get('question')
        try:
            number = int(question_param)
        except (TypeError, ValueError):
            number = 1
        variants_list = json.loads(active_test.variants)
        if number < 1:
            number = 1
        elif number > len(variants_list):
            number = len(variants_list)
        current_variant = variants_list[number - 1]
        question = current_variant['question']
        question_variants = current_variant['variants']
        your_answer = current_variant['your_answer']
        context = {
            'test_id': active_test.id,
            'question': question,
            'variants': question_variants,
            'your_answer': your_answer,
            'current_question': number,
            'all_question': len(variants_list),
            'questions_range': range(1, len(variants_list) + 1)
        }
        return render(request, 'tests/testing.html', context)
    except:
        return redirect(reverse('tests'))


@csrf_protect
def testing_save(request, id):
    active_test = get_object_or_404(ActiveTest, id=id, user=request.user)
    number = request.GET.get('number')
    try:
        number = int(number)
        if number < 1:
            return HttpResponseBadRequest("Неверный номер вопроса.")
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Неверный номер вопроса.")
    new_your_answer = request.POST.get('your_answer', '')
    new_your_answer_list = new_your_answer.split(',')
    variants_list = json.loads(active_test.variants)
    if number > len(variants_list):
        return HttpResponseBadRequest("Неверный номер вопроса.")
    variants_list[number - 1]['your_answer'] = new_your_answer_list
    active_test.variants = json.dumps(variants_list)
    active_test.save()
    finish = request.GET.get('finish')
    if finish:
        return HttpResponseRedirect(reverse('finish_test', args=[active_test.id]))
    return HttpResponseRedirect(reverse('testing', args=[active_test.id]) + f'?question={number + 1}')


@csrf_protect
def testing_finish_test(request, id):
    active_test = get_object_or_404(ActiveTest, id=id, user=request.user)
    variants_list = json.loads(active_test.variants)
    questions = []
    for item in variants_list:
        question = item['question']
        variants = item['variants']
        answer = item['answer']
        your_answer = item.get('your_answer', [])
        questions.append({
            "question": question,
            "variants": variants,
            "answer": answer,
            "your_answer": your_answer
        })
    return render(request, 'tests/finish_test.html', {"questions": questions})


@csrf_protect
def results(request):
    result = ActiveTest.objects.filter(user=request.user)
    return render(request, 'result/index.html', {'results': result})


def get_results(request, id):
    res = get_object_or_404(Result, id=id, user=request.user)
    return render(request, 'result/get.html', {'results': res})


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        else:
            messages.error(request, form.errors)
    else:
        form = SignUpForm()
    return render(request, 'facecontrol/register.html', {'form': form})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(UserProfile, email=form.cleaned_data['email'])
            if not user.check_password(form.cleaned_data['password']):
                return redirect('/login/')
            else:
                response = redirect('/home/')
                access_token = get_token(user)
                response.set_cookie('access_token', access_token, max_age=3600)
                return response
    else:
        form = LoginForm()
    return render(request, 'facecontrol/login.html', {'form': form})


@csrf_protect
def logout_view(request):
    response = redirect('/login/')
    response.set_cookie('access_token', None, max_age=0)
    response.set_cookie('refresh_token', None, max_age=0)
    return response
