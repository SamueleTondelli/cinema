"""
URL configuration for cinema project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from .initcmds import *
from .views import *
from movies.recommendation import *
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^$|^\/$|^home\/$", home,name="home"),
    path("login/", auth_view.LoginView.as_view(), name="login"),
    path("logout/", auth_view.LogoutView.as_view(), name="logout"),
    path("register/", CreateUserView.as_view(), name="register"),
    path("registermanager/", CreateManagerView.as_view(), name="registermanager"),

    path("movies/", include("movies.urls"))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Uncomment this line to automatically create the groups with the appropriate permissions
#init_groups()

# Uncomment these lines to delete and fill the database with example values
#erase_db()
#init_db()
