from django.contrib import admin
from .models import *

@admin.register(Interview)
class AnimalAdmin(admin.ModelAdmin):
    pass


@admin.register(Question)
class AnimalTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Answer)
class ImageAnimalAdmin(admin.ModelAdmin):
    pass


# @admin.register(UserAnswer)
# class ImageAnimalAdmin(admin.ModelAdmin):
#     pass
