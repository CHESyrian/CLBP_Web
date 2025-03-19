from django.db import models

# Create your models here.
class Mechanism_Data(models.Model):
    MechanismID     = models.CharField(primary_key=True, max_length=6, unique=True)
    Ownership       = models.CharField(max_length=48, blank=True, default='D')
    Disposal        = models.CharField(max_length=120, blank=True, default='D')
    Brand           = models.CharField(max_length=320, blank=True, default='D')
    Model           = models.CharField(max_length=320, blank=True, default='D')
    Type            = models.CharField(max_length=320, blank=True, default='D')
    Fuel_Limit      = models.IntegerField(blank=True, default=0)
    Repair_Limit    = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return str(self.MechanismID)


class Statements(models.Model):
    Statement_ID    = models.CharField(primary_key=True, unique=True, max_length=128)
    Requests_No     = models.CharField(max_length=320, blank=True, default='D')
    Statement_No    = models.CharField(max_length=3, blank=True, default='D')
    SubBalance      = models.CharField(max_length=32, blank=True, default='D')
    Statement_Value = models.IntegerField(blank=True, default=0)
    Statement_Type  = models.CharField(max_length=6, blank=True, default='D')
    Year            = models.CharField(max_length=4, blank=True, default='D')

    def __str__(self):
        return str(self.Statement_ID)


class Repair_Requests(models.Model):
    Request_ID     = models.CharField(primary_key=True, unique=True, max_length=16)
    Request_No     = models.CharField(max_length=10, blank=True, default='D')
    Request_Date   = models.DateField(auto_now=False, auto_now_add=False)
    Year           = models.CharField(max_length=16, blank=True, default='D')
    Month          = models.CharField(max_length=16, blank=True, default='D')
    Day            = models.CharField(max_length=16, blank=True, default='D')
    Mechanism_No   = models.ForeignKey(Mechanism_Data, on_delete=models.CASCADE, blank=True, default='D')
    KiloMeters     = models.IntegerField(blank=True, default=0)
    Ownership      = models.CharField(max_length=48, blank=True, default='D')
    Disposal       = models.CharField(max_length=120, blank=True, default='D')
    Model          = models.CharField(max_length=320, blank=True, default='D')
    Expected_Cost  = models.IntegerField(blank=True, default=0)
    Approval       = models.IntegerField(blank=True, default=0)
    Exchange_Date  = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    Driver         = models.CharField(max_length=64, blank=True, default='D')
    Real_Cost      = models.IntegerField(blank=True, default=0)
    Repair_Type    = models.CharField(max_length=16, default='صيانة طارئة')
    Status         = models.CharField(max_length=32, blank=True, default='D')
    Statement      = models.CharField(max_length=64, blank=True, default='D')

    def __str__(self):
        return str(self.Request_ID)


class Mechanisms_Repairs(models.Model):
    Request_ID   = models.ForeignKey(Repair_Requests, on_delete=models.CASCADE, default='D')
    Mechanism_No = models.CharField(max_length=6, blank=True, default='D')
    Request_Date = models.DateField(auto_now=False, auto_now_add=False, blank=True, null=True)
    Year         = models.CharField(max_length=4, blank=True, default='D')
    Month        = models.CharField(max_length=2, blank=True, default='D')
    Day          = models.CharField(max_length=2, blank=True, default='D')
    KiloMeters   = models.CharField(max_length=6, blank=True, default='D')
    Part_Repair  = models.CharField(max_length=120, blank=True, default='D')
    Part_Count   = models.IntegerField(blank=True, default=0)
    Part_Type    = models.CharField(max_length=32, blank=True, default='D')
    Cost         = models.IntegerField(blank=True, default=0)
    Receipt_No   = models.CharField(max_length=6, blank=True, default='D')
    Store        = models.CharField(max_length=64, blank=True, default='D')


    def __str__(self):
        return self.Part_Repair


class Parts_and_Repaires(models.Model):
    Name = models.CharField(max_length=320, blank=True, default='D')
    Type = models.CharField(max_length=320, blank=True, default='D')

    def __str__(self):
        return self.Name


class Drivers(models.Model):
    Driver_Name  = models.CharField(max_length=64, blank=True, default='D')
    Office       = models.CharField(max_length=64, blank=True, default='D')
    Mechanism_No = models.ForeignKey(Mechanism_Data, on_delete=models.CASCADE, blank=True, default='D')
    Disposal     = models.CharField(max_length=64, blank=True, default='D')

    def __str__(self):
        return self.Driver_Name


class Stores(models.Model):
    Store_Name = models.CharField(max_length=64, blank=True, default='D')
    Address    = models.CharField(max_length=128, blank=True, default='D')
    Email      = models.CharField(max_length=64, blank=True, default='D')
    PhoneNo    = models.CharField(max_length=16, blank=True, default='D')
    Mobile     = models.CharField(max_length=16, blank=True, default='D')

    def __str__(self):
        return self.Store_Name


class Receipts(models.Model):
    Receipt_ID    = models.CharField(primary_key=True, unique=True, max_length=64)
    Receipt_No    = models.CharField(max_length=16, blank=True, default='D')
    Request_ID    = models.ForeignKey(Repair_Requests, on_delete=models.CASCADE, blank=True, default='D')
    Receipt_Value = models.IntegerField(blank=True, default=0)
    Store_Name    = models.CharField(max_length=32, blank=True, default='D')
    Receipt_Date  = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.Receipt_ID}__{self.Store_Name}"


