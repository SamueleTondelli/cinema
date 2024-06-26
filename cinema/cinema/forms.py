from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group


class NewUserClient(UserCreationForm):
    user_group_name = "Clients"
    
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Clients")
        g.user_set.add(user)
        return user
    
    
class NewUserManager(UserCreationForm):
    user_group_name = "Managers"
    
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Managers")
        g.user_set.add(user)
        return user