from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Contractor)
admin.site.register(Partner)
admin.site.register(Station)
admin.site.register(Post)
admin.site.register(Card)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(UserTransaction)
