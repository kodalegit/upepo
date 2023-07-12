from django.contrib import admin
from .models import User, Likes, Comments

# Register your models here.
admin.site.register(User)
admin.site.register(Likes)
admin.site.register(Comments)