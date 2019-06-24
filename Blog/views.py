from django.shortcuts import render, redirect
from django.views import generic
from .models import Blog, Post, Subscription
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponseRedirect

# Create your views here.


class HomeView(generic.ListView):
    model = Blog
    template_name = 'Blog/home.html'

    def get_queryset(self):
        
        if self.request.user.is_authenticated:
            blogs = Blog.objects.exclude(user=self.request.user)
        else:
            blogs = Blog.objects.all()
        return blogs