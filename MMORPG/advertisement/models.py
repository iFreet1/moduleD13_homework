from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return str(self.name)


class PostCategory(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)


class Post(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ManyToManyField("Category", through="PostCategory")
    header = models.CharField(max_length=40)
    text = models.TextField()

    def get_absolute_url(self):
        return f'/posts/{self.id}'

    # def save(self, *args, **kwargs):
    #     self.user = args.user
    #     print(self.user)
    #     # super().save(*args, **kwargs)


class Response(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField()
    accepted = models.BooleanField()