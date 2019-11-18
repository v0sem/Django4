from django.contrib import admin
from datamodel.models import Game, Move

class GameAdmin(admin.ModelAdmin):
    list_display = ('cat_user', 'mouse_user', 'status')

# Register your models here.
admin.register(Game, GameAdmin)
admin.register(Move)