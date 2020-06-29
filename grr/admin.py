from django.contrib import admin
from .models import obj, user_obj, param, sens, values_sens
# Register your models here.
admin.site.register(obj)
admin.site.register(user_obj)
admin.site.register(param)
admin.site.register(sens)
admin.site.register(values_sens)
