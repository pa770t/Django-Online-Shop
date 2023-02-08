from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Customer

def create_customer(sender, instance, created, **kwargs):
    if created:
        # add user to Customer model
        Customer.objects.create(user=instance)
        # add user to Customer group
        group = Group.objects.get(name='Customer')
        instance.groups.add(group)

post_save.connect(create_customer, sender=User)