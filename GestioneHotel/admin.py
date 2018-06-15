from django.contrib import admin
from .models import *

admin.site.register(Albergatore)
admin.site.register(Indirizzo)
admin.site.register(Servizio)
admin.site.register(Hotel)
#admin.site.register(Camera)
admin.site.register(Prenotazione)
admin.site.register(ServiziDisponibili)

class ElencoServizi(admin.TabularInline):
    model=Camera.servizi.through

@admin.register(Camera)
class CameraAdmin(admin.ModelAdmin):
    inlines = (ElencoServizi,)
    exclude = ('servizi',)