from django.contrib import admin
from .models import User

admin.site.register(User)

#python birdrecognition/manage.py createsuperuser
#python birdrecognition/manage.py makemigrations  
# python birdrecognition/manage.py migrate