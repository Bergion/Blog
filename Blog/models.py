from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


# Create your models here.


class Blog(models.Model):

    user = models.OneToOneField(User, models.CASCADE, unique=True, related_name='blog')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('blog-detail', kwargs={'pk': self.pk})

class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='post')
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-pub_date', )


    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title

    
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscription')
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='subscription')

    class Meta:
        unique_together = ('user', 'blog')


class MarkedAsRead(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marked')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='marked')

    class Meta:
        unique_together = ('user', 'post')

@receiver(post_save, sender=User)
def save_blog(sender, instance, created, **kwargs):
    if created:
        name = "{}s Blog".format(instance.get_username())
        Blog.objects.create(user=instance, name=name)

@receiver(pre_delete, sender=Subscription)
def delete_marks(sender, instance, **kwargs):
    blogs_posts = Post.objects.filter(blog=instance.blog)
    MarkedAsRead.objects.filter(user=instance.user, post__in=blogs_posts).delete()


