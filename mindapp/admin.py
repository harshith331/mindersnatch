from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(option)
admin.site.register(Situation)
admin.site.register(Config)
admin.site.register(Player)
admin.site.register(SituationTimer)