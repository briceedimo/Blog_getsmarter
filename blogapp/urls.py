from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    # Pages publiques
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<slug:slug>/', views.article_detail, name='article_detail'),
    path('category/<slug:slug>/', views.articles_by_category, name='articles_by_category'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Actions sécurisées
    path('article/create/', views.article_form, name='article_form'),
    path('article/<slug:slug>/edit/', views.article_update, name='article_update'),
    path('article/<slug:slug>/confirm_delete/', views.article_confirm_delete, name='article_confirm_delete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
