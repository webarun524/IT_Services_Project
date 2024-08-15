from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)
    payment_terms = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    package = models.CharField(max_length=255)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    password = models.CharField(max_length=50)
    
    def __str__(self):
        return self.username