from django.db import models



class UserRole(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class Patient(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.firstname

class Writer(models.Model):
    name = models.CharField(max_length=200)
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return u'%s' % (self.name)

class Article(models.Model):
    text_title = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField(max_length=200, null=True, blank=True)
    refWriter = models.ForeignKey(Writer, on_delete=models.CASCADE)
    createdDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return u'[%s] : %s' % (self.refWriter,self.text_title)
