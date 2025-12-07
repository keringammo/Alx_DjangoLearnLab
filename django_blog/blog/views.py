from django.shortcuts import render
from django.db.models import Q
from .models import Post

def search_posts(request):
    query = request.GET.get('q')
    results = []
    if query:
        results = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(tags__name__icontains=query)
        ).distinct()
    return render(request, 'posts/search_results.html', {'posts': results, 'query': query})
