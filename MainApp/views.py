from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Snippet
from MainApp.forms import SnippetForm

def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == "GET":
        form = SnippetForm()
        return render(request, 'pages/add_snippet.html', {'form': form})
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("snippets_list")
        return render(request, 'add_snippet.html', {'form': form})


def snippets_page(request):
    context = {'snippets': Snippet.objects.values(), 'count': len(Snippet.objects.values())}
    return render(request, 'pages/view_snippets.html', context)

def snippet(request, id):
    for snippet in Snippet.objects.values():
        if snippet['id'] == id:
            lonely_snippet = snippet
    context = {"snippet": lonely_snippet}
    return render(request, 'pages/snippet.html', context)

# def create_snippet(request):
#    if request.method == "POST":
#        form = SnippetForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect("snippets_list")
#        return render(request,'add_snippet.html',{'form': form})