from django.shortcuts import render, redirect
from django.views import generic
from .models import Blog, Post, Subscription, MarkedAsRead
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib.sites.models import Site
# Create your views here.

@receiver(post_save, sender=Post)
def send_notification(sender, instance, **kwargs):
    recipient_list = Subscription.objects.filter(blog=instance.blog).exclude(user__email='')
    if recipient_list.exists():
        recipient_list = recipient_list.values_list('user__email', flat=True)
        subject = 'New post'
        domain = Site.objects.get_current().domain
        print(domain)
        post_url = "http://{0}:8000{1}".format(domain, instance.get_absolute_url())
        message = render_to_string('email/notification.html', {'blog':instance.blog, 'post_url':post_url})
        send_mail(subject, message=message, from_email='Blog', recipient_list=recipient_list)



class HomeView(generic.ListView):
    model = Blog
    template_name = 'Blog/home.html'

    def get_queryset(self):
        
        if self.request.user.is_authenticated:
            blogs = Blog.objects.exclude(user=self.request.user)
        else:
            blogs = Blog.objects.all()
        return blogs


class BlogDetailView(generic.DetailView):
    model = Blog
    
    def post(self, request, *args, **kwargs):
        blog = self.get_object()
        subscription, created = Subscription.objects.get_or_create(user=request.user, blog=blog)
        if not created:
            subscription.delete()

        return redirect(blog.get_absolute_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['subbed'] = Subscription.objects.filter(Q(user=self.request.user) & Q(blog=self.get_object())).exists()
            return context
        except TypeError:
            return context


class PostDetailView(generic.DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('sign-in')
    model = Post
    fields = ('title', 'content', )
    
    def get_success_url(self):
        return self.request.user.blog.get_absolute_url()

    def form_valid(self, form):
        form.instance.blog = self.request.user.blog
        return super().form_valid(form)


class PostListView(LoginRequiredMixin, generic.ListView):
    login_url = reverse_lazy('sign-in')
    model = Post

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.POST['id'])
        MarkedAsRead.objects.create(user=request.user, post=post)
        return redirect(reverse('news'))

    def get_queryset(self):
        subscribed_blogs = Blog.objects.filter(subscription__user=self.request.user)
        posts = Post.objects.filter(blog__in=subscribed_blogs).exclude(marked__user=self.request.user)
        return posts