from django.shortcuts import render, redirect, reverse
from django.template import loader
from django.http import HttpResponse
from django.contrib import messages
from django.db.models.deletion import ProtectedError
import logging

logger = logging.getLogger('mqtt')



class ObjectListMixin:
    model = None
    template = None
    context = None

    def get(self, request):
        objects = self.model.objects.all()
        return render(request,
                      self.template,
                      context={self.context: objects})


def objectDetailRequest(request, model, template):
    if request.is_ajax():
        itemId = request.POST['itemid']
        if itemId:
            obj = model.objects.get(id=itemId)
            t = loader.get_template(template)
            return t.render({model.__name__.lower(): obj})


def get_object_or_none(model, **kwargs):
    logger.debug(type(model))
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        logger.debug("OBJECTDOESTNOTEXIST!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        return None
    except:
        logger.debug("WTF!!!!!!!!!!!!!@#$@#%#$%@#")


class ObjectCreateMixin:
    form = None
    template = None
    redirect_url = None

    def get(self, request):
        form = self.form
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form(request.POST)
        if bound_form.is_valid():
            new_obj = bound_form.save()
            messages.success(request, 'Вы cоздали ' + str(new_obj))
            return redirect(self.redirect_url)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        bound_form = self.model_form(instance=obj)

        return render(request,  self.template,
                      context={self.model_form.__name__.lower(): bound_form,
                               self.model.__name__.lower(): obj})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)
        bound_form = self.model_form(request.POST, instance=obj)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            messages.info(request, 'Вы изменили ' + str(new_obj))

            return redirect("{}_list_url".format(self.model.__name__.lower()))
        return render(request, self.template,
                      context={self.model_form.__name__.lower(): bound_form,
                               self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        return render(request,  self.template,
                      context={self.model.__name__.lower(): obj})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)

        try:
            obj.delete()
            messages.info(request, 'Вы удалили ' + str(obj))
            return redirect("{}_list_url".format(self.model.__name__.lower()))
        except ProtectedError:
            messages.error(
                request, 'Вы не можете удалить {0}. Ошибка: Наличие транзакций или клиентов у контрагента'.format(obj))
            return redirect("{}_list_url".format(self.model.__name__.lower()))

        return redirect("{}_list_url".format(self.model.__name__.lower()))


class ObjectDisableMixin:
    model = None
    template = None

    def get(self, request, id):
        obj = self.model.objects.get(id=id)
        return render(request,  self.template,
                      context={self.model.__name__.lower(): obj})

    def post(self, request, id):
        obj = self.model.objects.get(id=id)

        if obj.is_active:
            obj.is_active = False
            obj.save()
            messages.info(request, 'Вы отключили {0}'.format(obj))
            return redirect("{}_list_url".format(self.model.__name__.lower()))

        else:
            messages.warning(
                request, 'Вы не можете отключить {0}.<br>Ошибка: Уже отлючена'.format(obj))
            return redirect("{}_list_url".format(self.model.__name__.lower()))
