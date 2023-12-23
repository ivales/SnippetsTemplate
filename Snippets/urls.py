from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='snippet_add'),
    path('snippets/list', views.snippets_page, name='snippets_list'),
    path('snippets/user', views.snippets_user, name='snippets_user'),
    path('snippet/<int:id>', views.snippet, name='snippet'),
    path('snippet/delete/<int:id>', views.snippet_delete, name='snippet_delete'),
    path('snippet/update/<int:id>', views.snippet_update, name='snippet_update'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path ('auth/register', views.create_user, name='register')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
