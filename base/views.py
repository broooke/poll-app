from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Vote, Question, Choice, Customer
from .forms import voteForm, voteForm1
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.db.models import Count
from django.forms import inlineformset_factory
from django.core.paginator import Paginator

# Create your views here.

def main(request):
    polls = Question.objects.all()
    search_term=''
    
    if 'name' in request.GET:
        polls=polls.order_by('question_text')
    elif 'date' in request.GET:
        polls=polls.order_by('pub_date')
    elif 'search' in request.GET:
        search_term = request.GET['search']
        polls = polls.filter(question_text__icontains=search_term)
    
    paginator = Paginator(polls, 2)  # Show 6 contacts per page
    page = request.GET.get('page')
    polls_all = paginator.get_page(page)

    get_dict_copy = request.GET.copy()
    params = get_dict_copy.pop('page', True) and get_dict_copy.urlencode()

    context = {'polls':polls,'search_term': search_term,'polls_all':polls_all,'params':params}
    return render(request,'main.html', context)

def voteView(request, poll_id):
    poll = Question.objects.get(id=poll_id)
    try:
        selected_choice = poll.choice_set.get(pk=request.POST['choice'])
    except:
        print('Error')
    else:
        selected_choice.votes+=1
        selected_choice.save()
        return redirect('result', poll_id=poll_id)
    
    context = {'poll':poll}

    return render(request,'vote.html', context)

def resultView(request, poll_id):
    poll = Question.objects.get(id=poll_id)

    context = {'poll':poll}

    return render(request, 'result.html', context)

def createView(request):
    PollFormSet = inlineformset_factory(Question,Choice,fields=('choice_text',))
    question = Question.objects.get(id=1)
    form = PollFormSet(queryset=Choice.objects.none(),instance=question)
    if request.method == 'POST':
        form = PollFormSet(request.POST,instance=question)
        if form.is_valid():
            form.save()
            return redirect('main')
    
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
    poll = get_object_or_404(Question, id=poll_id)
    poll.delete()
    return redirect('main')

def editPollView(request, poll_id):
    poll = Question.objects.get(id=poll_id)
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







