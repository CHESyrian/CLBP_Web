from enum import auto
from django.db import models


class Main_Balance(models.Model):
    Year     = models.CharField(primary_key=True, unique=True, max_length=4)
    Volume   = models.IntegerField(blank=True, default=0)
    Duration = models.CharField(max_length=16, blank=True, default='D')

    def __str__(self):
        return self.Year


class SubBalances(models.Model):
    SubBalance_ID = models.CharField(primary_key=True, unique=True, max_length=128)
    Account       = models.CharField(max_length=64, blank=True, default='D')
    Year          = models.ForeignKey(Main_Balance, on_delete=models.CASCADE)
    Volume        = models.IntegerField(blank=True, default=0)
    Duration      = models.CharField(max_length=16, blank=True, default='D')

    def __str__(self):
        return self.Account


class SubBalance_Items(models.Model):
    SubBalanceItem_ID  = models.CharField(primary_key=True, unique=True, max_length=128)
    Year               = models.ForeignKey(Main_Balance, on_delete=models.CASCADE)
    Account            = models.ForeignKey(SubBalances, on_delete=models.CASCADE)
    Item               = models.CharField(max_length=64, blank=True, default='D')
    Volume             = models.IntegerField(blank=True, default=0)
    Duration           = models.CharField(max_length=16, blank=True, default='D')

    def __str__(self):
        return f'{self.Account}_{self.Year} - {self.Item}'


class Exchange_Orders(models.Model):
    Order_ID         = models.CharField(primary_key=True, unique=True, max_length=128)
    Order_No         = models.CharField(max_length=4, blank=True, default='D')
    Order_Date       = models.DateField(auto_now=False, auto_now_add=False)
    Order_Value      = models.IntegerField(blank=True, default=0)
    Year             = models.ForeignKey(Main_Balance, on_delete=models.CASCADE)
    SubBalance       = models.ForeignKey(SubBalances, on_delete=models.CASCADE)
    SubBalanceItem   = models.ForeignKey(SubBalance_Items, on_delete=models.CASCADE)
    Creditor_Acc     = models.CharField(max_length=64, blank=True, default='D')
    Creditor_No      = models.CharField(max_length=64, blank=True, default='D')
    Debtor_Acc       = models.CharField(max_length=64, blank=True, default='D')
    Debtor_No        = models.CharField(max_length=64, blank=True, default='D')
    Check_No         = models.CharField(max_length=64, blank=True, default='D')
    Check_Date       = models.DateField(auto_now_add=False, auto_now=False)
    Recipient        = models.CharField(max_length=64, blank=True, default='D')

    def __str__(self):
        return self.Order_ID