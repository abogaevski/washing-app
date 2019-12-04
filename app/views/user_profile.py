from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages

from app.models import UserProfile
from app.forms import UserProfileForm

class UserProfileUpdate(View):
    def get(self, request):
        bound_form = UserProfileForm(instance=request.user.profile)

        return render(  request, 
                        "app/user_profile/user_profile_update.html",
                        context={   "profile_form": bound_form
                                }
                        )
    def post(self, request):
        bound_form = UserProfileForm(   request.POST,
                                        instance=request.user.profile)
        
        if bound_form.is_valid():
            new_user_profile = bound_form.save()
            messages.info(request, 'Вы изменили профиль: ' + str(new_user_profile))

            return redirect("app_url")
        return render(  request, 
                        "app/user_profile/user_profile_update.html",
                        context={"profile_form": bound_form})
