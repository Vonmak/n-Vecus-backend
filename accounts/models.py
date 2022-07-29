from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    roles_choices =(('customer','customer'),('vendor','vendor'))
    roles= models.CharField(choices=roles_choices, max_length=255, default='customer')
    phone= models.CharField(max_length=12)

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    bio = models.CharField(max_length=250)
    # email = models.EmailField(null=True, max_length=250)
    location= models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user(sender, instance, created, dispatch_uid="customer", **kwargs):
        if instance.roles=='customer':
            if created:
                Customer.objects.get_or_create(user = instance)

    @receiver(post_save, sender=User)
    def save_admin(sender, instance, **kwargs):
        if instance.roles=='customer':
            instance.customer.save()

    def save_profile(self):
            self.save()

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vendor')
    bio = models.CharField(max_length=250)
    # email= models.EmailField(max_length=100)
    location= models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_vendor(sender, instance, created, dispatch_uid="vendor", **kwargs):
        if instance.roles=='vendor':
            if created:
                Vendor.objects.get_or_create(user = instance)

    @receiver(post_save, sender=User)
    def save_admin(sender, instance, **kwargs):
        if instance.roles=='vendor':
            instance.vendor.save()

    def save_profile(self):
            self.save()
 