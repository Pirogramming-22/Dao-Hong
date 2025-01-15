import json
from django.shortcuts import render, get_object_or_404, redirect
from .models import Idea, DevTool
from django.views.decorators.http import require_POST
from .forms import IdeaForm, DevToolForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')  # 홈페이지 또는 대시보드로 리다이렉트
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # 로그인 성공 후 리다이렉트
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def idea_list(request):
    ideas = Idea.objects.all()
    for idea in ideas:
        idea.starred = idea.is_starred(request.user)
    return render(request, 'ideas/idea_list.html', {'ideas': ideas})

def idea_new(request):
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm()
    return render(request, 'ideas/idea_new.html', {'form': form})

def idea_detail(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    return render(request, 'ideas/idea_detail.html', {'idea': idea})

def idea_edit(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    if request.method == "POST":
        form = IdeaForm(request.POST, request.FILES, instance=idea)
        if form.is_valid():
            idea = form.save()
            return redirect('idea_detail', pk=idea.pk)
    else:
        form = IdeaForm(instance=idea)
    return render(request, 'ideas/idea_edit.html', {'form': form})

def devtool_list(request):
    devtools = DevTool.objects.all()
    return render(request, 'ideas/devtool_list.html', {'devtools': devtools})

def devtool_new(request):
    if request.method == "POST":
        form = DevToolForm(request.POST)
        if form.is_valid():
            devtool = form.save()
            return redirect('devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm()
    return render(request, 'ideas/devtool_new.html', {'form': form})

def devtool_detail(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    ideas = Idea.objects.filter(devtool=devtool)
    return render(request, 'ideas/devtool_detail.html', {'devtool': devtool, 'ideas': ideas})

def devtool_edit(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    if request.method == "POST":
        form = DevToolForm(request.POST, instance=devtool)
        if form.is_valid():
            devtool = form.save()
            return redirect('devtool_detail', pk=devtool.pk)
    else:
        form = DevToolForm(instance=devtool)
    return render(request, 'ideas/devtool_edit.html', {'form': form})

@require_POST
def idea_delete(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    idea.delete()
    return redirect('idea_list')

@require_POST
def devtool_delete(request, pk):
    devtool = get_object_or_404(DevTool, pk=pk)
    devtool.delete()
    return redirect('devtool_list')

@csrf_exempt
def change_interest(request):
    import json
    data = json.loads(request.body)
    idea = get_object_or_404(Idea, pk=data['id'])
    idea.interest += data['delta']
    idea.save()
    return JsonResponse({'new_interest': idea.interest})

@require_POST
def toggle_star(request):
    data = json.loads(request.body)
    idea_id = data['idea_id']
    idea = Idea.objects.get(id=idea_id)
    # is_starred 메서드로 상태 확인 후 처리
    currently_starred = idea.is_starred(request.user)
    # 새로운 상태를 반대로 설정
    new_starred_status = not currently_starred
    # 관련 데이터를 업데이트하는 로직 필요
    # 예: IdeaStar 모델 인스턴스의 starred 속성을 업데이트
    # idea.ideastar_set.update_or_create(user=request.user, defaults={'starred': new_starred_status})
    return JsonResponse({'starred': new_starred_status})



