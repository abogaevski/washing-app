from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

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
admin.site.register(EposPayment)


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)