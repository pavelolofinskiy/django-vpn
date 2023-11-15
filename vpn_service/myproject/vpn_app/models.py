from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    date_of_birth = models.DateField(null=True, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class UserSite(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    site_name = models.CharField(max_length=100)
    site_url = models.URLField()

    def __str__(self):
        return self.site_name
    
class UserSiteTraffic(models.Model):
    user_site = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    clicks = models.PositiveIntegerField(default=0)
    data_sent = models.FloatField(default=0)  
    data_received = models.FloatField(default=0)

    def __str__(self):
        return f"Traffic for {self.user_site.site_name}"