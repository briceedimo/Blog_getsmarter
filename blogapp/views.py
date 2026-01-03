from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from django.http import HttpResponseForbidden

from .models import Article, Category
# from .forms import ArticleForm


def home(request):
    articles = Article.objects.filter(
        status='published',
        published_at__lte=timezone.now()
    ).order_by('-published_at')[:5]

    return render(request, 'blogapp/home.html', {'articles': articles})


