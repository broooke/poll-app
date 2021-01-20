from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Vote
from .forms import voteForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages

# Create your views here.

def main(request):
    polls = Poll.objects.all()
    context = {'polls':polls}
    return render(request,'main.html', context)

def voteView(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
        
    if request.method == 'POST':
        action = request.POST['poll']
        if action == 'option1':
            poll.one_choice_count+=1
        elif action == 'option2':
            poll.two_choice_count+=1
        else:
            poll.three_choice_count+=1
        poll.save()
        return redirect('main')
    else:
        form = voteForm()
        
    context = {'poll':poll}

    return render(request,'vote.html', context)

def resultView(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    context = {'poll':poll}

    return render(request, 'result.html', context)

def createView(request):
    if request.method == 'POST':
        form = voteForm(request.POST)
        if form.is_valid():
            form_save = form.save(commit=False)
            form_save.user = request.user
            form_save.save()
            return redirect('main')
    else:
        form = voteForm()
    
    context = {'form':form}

    return render(request,'create.html', context)

def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('main')
            else:
                print('Error login!')
    else:
        form = AuthenticationForm()

    context = {'form':form}

    return render(request,'login.html', context)

def signUpView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
        username = request.POST.get('username')
        password = request.POST.get('password1')
        user = authenticate(username=username,password=password)
        login(request,user)
        return redirect('main')
    else:
        form = UserCreationForm()

    context = {'form':form}

    return render(request,'signup.html', context)

def logOutView(request):
    logout(request)
    return redirect('login')

def deletePollView(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    poll.delete()
    return redirect('main')

def editPollView(request, poll_id):
    poll = Poll.objects.get(id=poll_id)
    form = voteForm(instance=poll)
    if request.method == 'POST':
        form = voteForm(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('main')

    context = {'form':form}

    return render(request,'editpoll.html', context)

def pollUserView(request):
    user = request.user
    polls = Poll.objects.filter(user=user)

    context = {'polls':polls}

    return render(request, 'userpolls.html', context)







