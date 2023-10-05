from django.db import models
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author =  models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = "blog_images/")
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

class Like(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Like)
def add_like(sender, instance=None, created = False, **kwargs):
    if created:
        post = BlogPost.objects.get(id=instance.post.id)
        post.likes +=1
        post.save()

