
from django.contrib import admin
from django.urls import path
from Blog import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(), name='home'),
    path('blog/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),
    path('post/<int:pk>/',views.PostDetailView.as_view(), name='post-detail'),
    path('post/create/', views.PostCreateView.as_view(), name='post-create'),
    path('news/', views.PostListView.as_view(), name='news'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('sign-in', auth_views.LoginView.as_view(template_name='Blog/login.html'), name='sign-in'),
]
