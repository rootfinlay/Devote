from django.contrib import admin
from .models import Voters

# Register your models here.
class VotersAdmin(admin.ModelAdmin):
    list_display = (['name', 'identifier'])
    search_fields = (['name', 'identifier', 'block_content'])

admin.site.register(Voters, VotersAdmin)