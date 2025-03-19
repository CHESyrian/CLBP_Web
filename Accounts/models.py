from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class User_Activation(models.Model):
    User_Name     = models.ForeignKey(User, on_delete=models.CASCADE)
    U_Office      = models.CharField(max_length=320, null=True)
    U_Section     = models.CharField(max_length=320, null=True)
    U_Job         = models.CharField(max_length=320, null=True)
    Is_Active     = models.BooleanField()
    Perm_Sections = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.User_Name.username
