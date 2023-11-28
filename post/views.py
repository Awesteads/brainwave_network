from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .forms import NewPostForm, EditPostForm, CommentForm
from .models import Category, Post, Comment


def posts(request):
    query = request.GET.get('query', '')
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()
    posts = Post.objects.all()

    if category_id:
        posts = posts.filter(category_id=category_id)

    if query:
        posts = posts.filter(Q(titulo__icontains=query) | Q(texto__icontains=query))

    return render(request, 'post/posts.html', {
        'posts': posts,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user  # ou qualquer método que você usa para obter o usuário atual
            comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})

def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()
    else:
        comment_form = CommentForm()

    comments = Comment.objects.filter(post=post)

    return render(request, 'post.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })


@login_required
def new(request):
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()

            return redirect('post:detail', pk=post.id)
    else:
        form = NewPostForm()

    return render(request, 'create_post.html', {
        'form': form,
        'title': 'New post',
    })

@login_required
def edit(request, pk):
    post = get_object_or_404(Post, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()

            return redirect('post:detail', pk=post.id)
    else:
        form = EditPostForm(instance=post)

    return render(request, 'post.html', {
        'form': form,
        'title': 'Edit post',
    })

@login_required
def delete(request, pk):
    post = get_object_or_404(Post, pk=pk, created_by=request.user)

    if request.method == 'POST':
        post.delete()
        return redirect('core:brainwave')

    # Se o usuário não for o criador do post, levante uma exceção de permissão
    raise PermissionDenied

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Verifica se o usuário já curtiu o post
    liked = post.likes.filter(id=request.user.id).exists()

    if liked:
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    likes_count = post.likes.count()

    return JsonResponse({'liked': not liked, 'likes_count': likes_count})

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Verifica se o usuário já curtiu o comentário
    liked = comment.likes.filter(id=request.user.id).exists()

    if liked:
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    likes_count = comment.likes.count()

    return JsonResponse({'liked': not liked, 'likes_count': likes_count})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    # Verifica se o usuário logado é o autor do comentário
    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Comentário excluído com sucesso.')
    else:
        messages.error(request, 'Você não tem permissão para excluir este comentário.')

    # Redireciona de volta à página do post ou para onde você desejar
    return redirect('post:detail', pk=comment.post.pk)


