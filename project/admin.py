from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Player)
admin.site.register(Manager)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(PlaysIn)
admin.site.register(Invitation)
admin.site.register(MatchRequest)