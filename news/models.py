from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    categoryname = models.CharField(max_length=100)
    def __str__(self):
        return self.categoryname



class Newspost(models.Model):
    posttitle = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    postdetail = models.TextField()
    postimage = models.FileField(null=True)
    postdate = models.DateField()
    def __str__(self):
        return self.posttitle+" "+self.category.categoryname


class Comment(models.Model):
    newspost = models.ForeignKey(Newspost, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    emailid = models.CharField(max_length=40)
    commentmsg = models.CharField(max_length=1000)
    cdate = models.DateField()
    status = models.CharField(max_length=20)
    def __str__(self):
        return self.commentmsg

class Contact(models.Model):
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=15)
    emailid = models.CharField(max_length=40)
    message = models.CharField(max_length=300)
    mdate = models.DateField()
    isread = models.CharField(max_length=10)
    def __str__(self):
        return self.name