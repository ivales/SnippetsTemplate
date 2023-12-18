from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page),
    path('snippets/add', views.add_snippet_page, name='snippet_add'),
    path('snippets/list', views.snippets_page, name='snippets_list'),
    path('snippet/<int:id>', views.snippet, name='snippet'),
    path('snippet/delete/<int:id>', views.snippet_delete, name='snippet_delete'),
    path('snippet/update/<int:id>?<str:name>&<str:code>', views.snippet_update, name='snippet_update')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
