from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):

    fields = 'title', 'text', 'author', # 'created', 'updated',
    list_display = 'title', 'created', 'updated',



# admin.site.register(Note, NoteAdmin)




