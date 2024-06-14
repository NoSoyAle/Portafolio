from django.urls import path
from django.contrib.auth import views as auth_views
#  password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from .views import  dates, LikeView, exit, register,buscar, HomeListView, PostDetailView, CategoryListView, AutorListView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    #PAGINA DE INICIO
    path('', HomeListView.as_view() , name='home'),
    #DETALLE DEL POST
    path('post/<pk>', PostDetailView.as_view() , name='post'),   
    #PAGINA FILTRADO DE CATEGORIAS
    path('category/', CategoryListView.as_view(), name='category' ),    
    #PAGINA FILTRADO DE AUTOR
    path('author/', AutorListView.as_view(), name='author'),
    #PAGINA FILTRADO POR FECHA
    path('dates/<int:month_id>/<int:year_id>', dates, name='dates'),
    #LIKES DE UN POST
    path('like/<int:pk>', LikeView, name='like_post'),
    path('logout/', exit, name='exit'),
    path('register/', register, name='register'),
    path('create/', PostCreateView.as_view(), name='create'),
    #EDitar Post
    path('update/<int:pk>', PostUpdateView.as_view(), name='update'),
    #Eliminar Post
    path('delete/<int:pk>', PostDeleteView.as_view(), name='delete'),
    #Buscar post
    path('buscar/', buscar, name='buscar'),
    #Recuperar tu contraseñaq
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]