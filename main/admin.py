from django.contrib import admin
from .models import Admin, User, Developer, Bug, Category, Priority

admin.site.register(Admin)
admin.site.register(User)
admin.site.register(Developer)
admin.site.register(Bug)
admin.site.register(Category)
admin.site.register(Priority)

