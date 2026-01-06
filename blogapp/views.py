from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.http import HttpResponseForbidden

from .models import Article, Category, ContactMessage
from django.contrib import messages
from .forms import ArticleForm

# Vue pour la page d’accueil
def home(request):
    articles = Article.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).order_by('-published_at')[:5]

    return render(request, 'blogapp/home.html', {'articles': articles})

# Liste des articles
def article_list(request):
    articles = Article.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    )
    return render(request, 'blogapp/article_list.html', {'articles': articles})


# Détail d'un article
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, status='published')
    return render(request, 'blogapp/article_detail.html', {'article': article})


# Création d'un article

@login_required
@permission_required('blogapp.article_form', raise_exception=True)
def article_form(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.published_at = timezone.now()
            article.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm()
    return render(request, 'blogapp/article_form.html', {'form': form})


# Modification d'un article

@login_required
@permission_required('blogapp.change_article', raise_exception=True)
def article_update(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.user != article.author and not request.user.is_superuser:
        return HttpResponseForbidden("Accès refusé")

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_detail', slug=article.slug)
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blogapp/article_form.html', {'form': form})


# Suppression d'un article

@login_required
def article_confirm_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.user != article.author and not request.user.is_superuser:
        return HttpResponseForbidden("Accès refusé")

    if request.method == 'POST':
        article.delete()
        return redirect('article_list')

    return render(request, 'blogapp/article_confirm_delete.html', {'article': article})


# Articles par catégorie
def articles_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(
        category=category,
        status='published',
        published_at__lte=timezone.now()
    )
    return render(request, 'blogapp/articles_by_category.html', {
        'category': category,
        'articles': articles
    })

# Page À propos
def about(request):
    return render(request, 'blogapp/about.html')

# Page Contact
def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message'],
        )
        messages.success(request, "Message envoyé avec succès.")
    return render(request, 'blogapp/contact.html')
