from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
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
           form = SnippetForm(initial={'name':lonely_snippet['name'], 'lang':lonely_snippet['lang'], 'code':lonely_snippet['code']})
           context = {"id":id,"form": form, "method": request.method}
           return render(request, 'pages/snippet.html', context)


def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, id=id)
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
