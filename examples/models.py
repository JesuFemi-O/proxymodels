from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.
# we are going to create a base user that can either be a spy or driver
#we wil create spy and driver user to inherit from base user
#we will overide save() in the subclasses such that 
#a defulat type in driver subclass user becomes driver 
#and default type in spyuser subclass becoems spy
#this is the concept of a proxy model in django
#you let Djnago know a model is proxy via the meta class
#proxy models don't lead to the creation of new tables differnt from 
#the model they are inheriting from

#the concept of proxy models require a base model and 1 or more other models inheriting from the base model
#the proxy models may require a manager to help them filter the basemodel queryset
#proxy models will require their own save() method to ovveride the base class method
#example of where to use proxy models is in situations where you have differnt types of users in you app
#e.g teacher and student



##NOTE:
#AbstractUser is a full User model, complete with fields, 
# as an abstract class so that you can inherit from it and add your own profile fields 
# and methods. 

#it is a best practice to not use django User model directly 
# we are advised to atleast inerit the abstractUser model instead.

# AbstractBaseUser only contains the authentication functionality, 
# but no actual fields: you have to supply them when you subclass.

#REMEBER TO SET AUTH_USER_MODEL = 'examples.User' in project settings.py else you might have issues!
class User(AbstractUser):
    #instead of using tuples to define choices 
    # we can also use a class that inherits from TextChoices
    class Types(models.TextChoices):
        SPY = "SPY", "Spy"
        DRIVER = "DRIVER", "Driver"
    
    type = models.CharField(_("Types"), max_length=58, choices=Types.choices, default=Types.SPY)

    ##first name and last name do not cover name patterns globally
    username = models.CharField(_("Name of User"), unique=True, blank=True, max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username":self.username})
    
    def __str__(self):
        return self.email


#A Manager is the interface through which database query operations are provided to Django models.
#  At least one Manager exists for every model in a Django application.


class SpyManager(models.Manager):
    #since it is inheriting from User the default queryset is the user query set
    #this means when we query spies we get all the users created in User
    #we want to be able to get only spy objects when we query this model
    #let's override it

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(self, *args, **kwargs).filter(type=User.Types.SPY)



class DriverManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(self, *args, **kwargs).filter(type=User.Types.DRIVER)

class Spy(User):
    #connect the spy manager to the spy model
    objects = SpyManager()
    
    #inform  django this model is a proxy
    class Meta:
        proxy=True
    
    def save(self, *args, **kwargs):
        #check if user already exist
        #this is important cos the save() method is triggered after updates too
        if not self.pk:
            self.type = User.Types.SPY
        return super().save(*args, **kwargs)


    #let's also write a method unique to only spies
    def whisper(self):
        return "spies whisper"



class Driver(User):
    #connect the driver manager to the driver mmodel
    objects = DriverManager()

    class Meta:
        proxy = True
    
    def save(self, *args, **kwargs):
        #check if user already exist
        #this is important cos the save() method is triggered after updates too
        if not self.pk:
            self.type = User.Types.DRIVER
        return super().save(*args, **kwargs)

    def speed(self):
        return "Drivers go faster"


#finally instead of overriding safe we can create a variable in our base user model
#e.g data_type = Types.SPY
#we can then pass this variable into the 'defualt=' for the types field
#in our sub classes all we need to do is override the value of this variable
#e.g in the driver model once we set:
#data_type = User.Types.Driver
#the defualt for any object created in tha class becomes driver. 
#this is far more maintainable!

#in the end we now have spy user, driver user and admin user. the admin user can change driver to spy and vice versa!