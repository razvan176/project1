from django.db import models

# Create your models here.
class Set(models.Model):
    set_name= models.CharField(max_length=264,unique=True)
    def __str__(self):
        return self.set_name
    
class Pmta(models.Model):
    set_name = models.ForeignKey(Set, on_delete=models.CASCADE)
    date= models.DateField()
    hour=models.CharField(max_length=20)
    number_send =models.CharField(max_length=20)
    ip =models.CharField(max_length=20)
    id_mint =models.CharField(max_length=20)
    def __str__(self):
        return f"{self.set_name.set_name} - {self.date} - {self.hour} - {self.number_send} - {self.ip} - {self.id_mint}"

class Mint(models.Model):
    set_name = models.ForeignKey(Set, on_delete=models.CASCADE)
    id_mint = models.CharField(max_length=20)
    open_rate =models.CharField(max_length=20)
    nr_clicks =models.CharField(max_length=20)
    nr_unsub=models.CharField(max_length=20)
    abuse=models.CharField(max_length=20)
    def __str__(self):
        return f"{self.set_name.set_name} - {self.id_mint}"
     
