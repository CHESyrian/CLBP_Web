from django.db import models


# Create your models here.
class Site_Dictionary(models.Model):
    Name = models.CharField(max_length=320, null=True)
    Code = models.CharField(max_length=320, null=True)

    def __str__(self):
        return self.Name


class User_Permissions(models.Model):
    Perm_Code = models.CharField(max_length=320, null=True)
    Perm_Name = models.CharField(max_length=320, null=True)
    Perm_URL  = models.CharField(max_length=32, null=True)

    def __str__(self):
        return self.Perm_Name
