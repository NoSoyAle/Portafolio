from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Category
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login

# Create your views here.
def home(request):

    if not request.session.get('items_per_page'):
        request.session['items_per_page'] = 2

    if request.method == 'GET' and 'items_per_page' in request.GET:
        request.session['items_per_page'] = int(request.GET['items_per_page'])

    items_per_page = request.session['items_per_page']

    posts_page = Paginator(Post.objects.filter(published=True), items_per_page)
    page = request.GET.get('page')
    posts = posts_page.get_page(page)
    aux = 'x' * posts.paginator.num_pages

    return render(request,'core/home.html', {'posts':posts, 'aux':aux})

# Detalle del Post
@login_required
def post(request, post_id):
    # post = Post.objects.get(id=post_id)
    try:
        post = get_object_or_404(Post, id=post_id)
        total_likes = post.total_likes()

        liked = False
        if post.likes.filter(id=request.user.id).exists():
            liked = True

        return render(request, 'core/detail.html', {'post':post, 'total_likes':total_likes, 'liked':liked})
    except:
        return render(request, 'core/404.html')


def register(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        user_creation_form = CustomUserCreationForm(data=request.POST)

        if user_creation_form.is_valid():
            user_creation_form.save()

            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)

            return redirect('/')

    return render(request, 'registration/register.html', data)


def exit(reuqest):
    logout(reuqest)
    return redirect('home')

# Filtrado por Categoría
def category(request, category_id):
    try:
        category = get_object_or_404(Category, id=category_id)
        return render(request, 'core/category.html', {'category':category})
    except:
        return render(request, 'core/404.html')

# Filtrado por Author
def author(request, author_id):
    try:
        author = get_object_or_404(User, id=author_id)
        return render(request, 'core/author.html', {'author':author})
    except:
        return render(request, 'core/404.html')

def dates(request, month_id, year_id):

    meses = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }

    if month_id > 12 or month_id < 1:
        return render(request, 'core/404.html')

    posts = Post.objects.filter(published=True, created__month=month_id, created__year=year_id)
    return render(request, 'core/dates.html', {'posts':posts, 'month':meses[month_id], 'year':year_id})

# Likes en un post
def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('post', args=[str(pk)]))
