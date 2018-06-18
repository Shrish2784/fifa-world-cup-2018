"""fifapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include

class Data:
    names = set()

    def collect_data(self):
        global names
        file = open('names')
        for f in file:
            l = list(f.split("\n"))
            self.names.add(l[0])

    def print_len(self):
        print(len(self.names))

d = Data()
d.collect_data()
d.print_len()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
]

