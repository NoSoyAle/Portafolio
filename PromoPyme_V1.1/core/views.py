from typing import Any
from django.db.models.query import QuerySet
from django.forms import BaseModelForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from .forms import CustomUserCreationForm, PostForm
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView  
#from django.contrib.auth.decorators import login_required


# Create your views here.

#Home
class HomeListView(ListView):
    model = Post
    paginate_by = 3
    template_name = 'core/home.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context



#def home(request):

#    if not request.session.get('items_per_page'):
#        request.session['items_per_page'] = 2

#    if request.method == 'GET' and 'items_per_page' in request.GET:
#        request.session['items_per_page'] = int(request.GET['items_per_page'])

#    items_per_page = request.session['items_per_page']

#    posts_page = Paginator(Post.objects.filter(published=True), items_per_page)
#    page = request.GET.get('page')
#    posts = posts_page.get_page(page)
#    aux = 'x' * posts.paginator.num_pages

#    return render(request,'core/home.html', {'posts':posts, 'aux':aux})









# Detalle del Post


class PostDetailView(DetailView):
    model = Post
    template_name = 'core/detail.html'



#@login_required

#def post(request, post_id):
    # post = Post.objects.get(id=post_id)
#    try:
#        post = get_object_or_404(Post, id=post_id)
#        total_likes = post.total_likes()
#
#        liked = False
#        if post.likes.filter(id=request.user.id).exists():
#            liked = True

#        return render(request, 'core/detail.html', {'post':post, 'total_likes':total_likes, 'liked':liked})
#    except:
#        return render(request, 'core/404.html')





# Filtrado por Categoría
class CategoryListView(ListView):
    model = Category
    template_name = 'core/category.html'

    def get_queryset(self):
        category_id = self.request.GET['cat']

        if category_id:
            return Post.objects.filter(category=category_id, published=True)
        
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['category']= Category.objects.get(id =  self.request.GET['cat'])
        return context



# Filtrado por Categoría
#def category(request, category_id):
#    try:
#        category = get_object_or_404(Category, id=category_id)
#        return render(request, 'core/category.html', {'category':category})
#    except:
#        return render(request, 'core/404.html')



class AutorListView(ListView):
    model = User
    template_name = 'core/author.html'

    def get_queryset(self):
        author_id = self.request.GET['aut']

        if author_id:
            return Post.objects.filter(author_id=author_id, published= True)
        
        return super().get_queryset()
    
    def get_context_data(self, **kwargs):
        context = super(AutorListView, self).get_context_data(**kwargs)
        context['author']= User.objects.get(id =  self.request.GET['aut'])
        return context



# Filtrado por Author
#def author(request, author_id):
#    try:
#        author = get_object_or_404(User, id=author_id)
#        return render(request, 'core/author.html', {'author':author})
#    except:
#        return render(request, 'core/404.html')











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

# Crear Post
class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    success_url = reverse_lazy('home')

#Edicion del Post    
class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name_suffix = 'update_form'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('update', args=[self.object.id]) + '?ok' 
       
    
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('home')