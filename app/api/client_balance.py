import json
from decimal import Decimal


from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from app.models import Card, Partner, Contractor

# TODO: Написать лог!
class ClientBalance(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            results = {
                "success": False,
                "error_message": "JSON syntax error"
            }
            return JsonResponse(results)
        try:
            action = data['action']
        except:
            results = {
                "success": False,
                "error_message": "No action defined"
            }
            return JsonResponse(results)
        try:
            ext_client_id = data['client_id']
        except: 
            results = {
                "success": False,
                "error_message": "No client defined"
            }
            return JsonResponse(results)

        try:
            partner = Partner.objects.get(name=ext_client_id)
        except ObjectDoesNotExist:
            results = {
                "success": False,
                "error_message": "Client {} not found".format(ext_client_id)
            }
            return JsonResponse(results)
        except MultipleObjectsReturned:
            results = {
                "success": False,
                "error_message": "Too many clients with id {}".format(ext_client_id) 
            }
            return JsonResponse(results)

        if partner:
            #TODO: Сделать привязку контрагента к профилю
            # if request.user.userprofile.contractor == partner.contractor:
            if action == "get_client_balance":

                results = {
                    "success": True,
                    "client_balance": partner.balance    
                }
                return JsonResponse(results)

            elif action == "inc_client_balance":
                
                try:
                    amount = data["amount"]
                except:
                    results = {
                        "success": False,
                        "error_message": "No amount defined for client {}".format(partner.name)
                    }
                    return JsonResponse(results)
                # TODO: Check dec amount
                partner.balance += Decimal(amount)
                # TODO: Create try
                partner.save()

                results = {
                    "success": True,
                    "client_balance": partner.balance
                }
                return JsonResponse(results)

            elif action == "dec_client_balance":
                
                try:
                    amount = data["amount"]
                except:
                    results = {
                        "success": False,
                        "error_message": "No amount defined for client {}".format(partner.name)
                    }
                    return JsonResponse(results)
                # TODO: Check dec amount
                partner.balance -= Decimal(amount)
                # TODO: Create try
                partner.save()

                results = {
                    "success": True,
                    "client_balance": partner.balance
                }
                return JsonResponse(results)

            else:
                pass
        else:
            pass

        
        results = {
            "success": False,
            "error_message": "Internal error"
        }
        return JsonResponse(results)
