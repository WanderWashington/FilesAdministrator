from django.contrib import admin
from .models import User
from .models import Address
from .models import File
from .models import FileHistory
from django.contrib.auth.models import Permission


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Address, admin.ModelAdmin)
admin.site.register(FileHistory, admin.ModelAdmin)
admin.site.register(File, admin.ModelAdmin)
