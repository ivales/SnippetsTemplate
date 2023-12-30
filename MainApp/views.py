from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from MainApp.models import Snippet, Comment



def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


@login_required
def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        return render(request, 'pages/add_snippet.html', {'form': form})
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()
            return redirect("snippets_list")
        return render(request, 'add_snippet.html', {'form': form})


def snippets_page(request):
    context = {'snippets': Snippet.objects.filter(public=True), 'count': Snippet.objects.filter(public=True).count()}
    return render(request, 'pages/view_snippets.html', context)


@login_required
def snippets_user(request):
    context = {'snippets': Snippet.objects.filter(user__username=request.user), 'count': Snippet.objects.filter(user__username=request.user).count()}
    return render(request, 'pages/view_snippets.html', context)


def snippet(request, id):
    for snippet in Snippet.objects.values():
        if snippet['id'] == id:
           lonely_snippet = snippet
           form = SnippetForm(initial={'name': lonely_snippet['name'], 'lang': lonely_snippet['lang'], 'code': lonely_snippet['code']})
           comment_form = CommentForm(initial={'snippet': Snippet.objects.get(pk=id)})
           context = {"id": id, "form": form, "method": request.method, "comment_form": comment_form, "comments":Comment.objects.filter(snippet__id=id), 'snippet': lonely_snippet}
           return render(request, 'pages/snippet.html', context)


@login_required
def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, id=id)
    if snippet['user'].username == request.user:
        snippet.delete()
    return redirect("/snippets/list")


def snippet_update(request, id):
    form = SnippetForm(request.POST)
    if form.is_valid():
        snippet = get_object_or_404(Snippet, id=id)
        snippet.name = form.cleaned_data.get("name")
        snippet.lang = form.cleaned_data.get("lang")
        snippet.code = form.cleaned_data.get("code")
        snippet.save()
        return redirect("snippets_list")


def logout(request):
    auth.logout(request)
    return redirect('home')


def login(request):
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)
       else:
           context = {
               'pagename': 'PythpnBin',
               'errors': ["wrong username or password"]
           }
           return render(request, 'pages/index.html', context)
   return redirect('home')


def create_user(request):
    context = {'pagename': "Регистрация пользователя"}
    if request.method == "GET":
        form = UserRegistrationForm()
        return render(request, 'pages/registration.html', {'form': form})
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
        return render(request, 'pages/registration.html', {'form': form})


@login_required()
def comment_add(request):
   if request.method == "POST":
       comment_form = CommentForm(request.POST)
       print(request)

       print(request.POST)
       if comment_form.is_valid():
           comment = comment_form.save(commit=False)
           comment.text = comment_form.cleaned_data.get('text')
           comment.author = request.user
           comment.snippet = comment_form.cleaned_data.get('snippet')
           comment.save()

       return redirect(f'/snippet/{comment.snippet.id}')

   raise Http404


@login_required
def comment_delete(request, id):
    if request.method == "POST":
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def comment_update(request, id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = get_object_or_404(Comment, id=id)
        comment.text = form.cleaned_data.get("text")
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))